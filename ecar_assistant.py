import sys
import os
import datetime
import sqlite3
import requests
import threading
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QPushButton, QLabel, 
                            QListWidget, QListWidgetItem, QSplitter, QMessageBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QIcon, QTextCursor
import pyttsx3
import pygame
from transformers import pipeline
from duckduckgo_search import DDGS

class SearchWorker(QThread):
    """Worker thread for search operations"""
    finished = pyqtSignal(str, list)
    
    def __init__(self, query):
        super().__init__()
        self.query = query
        
    def run(self):
        try:
            # Generate AI response
            ai_response = self.generate_ai_response(self.query)
            
            # Web search
            search_results = self.web_search(self.query)
            
            # Combine results
            self.finished.emit(ai_response, search_results)
        except Exception as e:
            self.finished.emit(f"Ошибка при поиске: {str(e)}", [])
    
    def generate_ai_response(self, query):
        try:
            # Initialize the model for text generation
            generator = pipeline('text-generation', model='sberbank-ai/rugpt3small_based_on_gpt2')
            
            # Generate response
            prompt = f"Вопрос: {query}\nОтвет:"
            result = generator(prompt, max_length=200, num_return_sequences=1)
            
            # Extract and clean up the response
            response = result[0]['generated_text'].replace(prompt, "").strip()
            
            # If response is too short or doesn't make sense, provide a fallback
            if len(response) < 20:
                return "Извините, не удалось сгенерировать подходящий ответ. Пожалуйста, проверьте результаты поиска ниже."
                
            return response
        except Exception as e:
            return f"Не удалось сгенерировать ответ с помощью AI: {str(e)}"
    
    def web_search(self, query):
        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=5):
                    results.append({
                        'title': r['title'],
                        'url': r['href'],
                        'snippet': r['body']
                    })
            return results
        except Exception as e:
            print(f"Ошибка при поиске в интернете: {str(e)}")
            return []

class IkarAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_db()
        self.init_tts()
        self.init_audio()
        self.show_welcome_message()
        
    def init_ui(self):
        self.setWindowTitle("ИКАР-Ассистент")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
            }
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
            QPushButton:pressed {
                background-color: #585b70;
            }
            QTextEdit, QListWidget {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                color: #cdd6f4;
            }
        """)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Input section
        input_label = QLabel("Введите запрос:")
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Например: Ошибка ФН при печати чека в 1С 8.3")
        self.input_text.setMaximumHeight(100)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.search_button = QPushButton("Найти решение")
        self.search_button.setIcon(QIcon.fromTheme("search"))
        self.search_button.clicked.connect(self.search)
        
        self.speak_button = QPushButton("Озвучить ответ")
        self.speak_button.setIcon(QIcon.fromTheme("audio-volume-high"))
        self.speak_button.clicked.connect(self.speak_response)
        self.speak_button.setEnabled(False)
        
        self.open_link_button = QPushButton("Открыть ссылку")
        self.open_link_button.setIcon(QIcon.fromTheme("web-browser"))
        self.open_link_button.clicked.connect(self.open_link)
        self.open_link_button.setEnabled(False)
        
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.speak_button)
        button_layout.addWidget(self.open_link_button)
        
        # Results section
        results_label = QLabel("Результат:")
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        
        # Links section
        links_label = QLabel("Найденные ссылки:")
        self.links_list = QListWidget()
        self.links_list.itemClicked.connect(self.select_link)
        
        # History section
        history_label = QLabel("История запросов:")
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_history_item)
        
        # Add widgets to layout
        main_layout.addWidget(input_label)
        main_layout.addWidget(self.input_text)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(results_label)
        main_layout.addWidget(self.results_text)
        
        # Create splitter for links and history
        bottom_splitter = QSplitter(Qt.Horizontal)
        
        links_widget = QWidget()
        links_layout = QVBoxLayout(links_widget)
        links_layout.addWidget(links_label)
        links_layout.addWidget(self.links_list)
        
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.addWidget(history_label)
        history_layout.addWidget(self.history_list)
        
        bottom_splitter.addWidget(links_widget)
        bottom_splitter.addWidget(history_widget)
        bottom_splitter.setSizes([500, 500])
        
        main_layout.addWidget(bottom_splitter)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Store search results
        self.current_links = []
    
    def init_db(self):
        # Create database if it doesn't exist
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ecar_history.db')
        self.conn = sqlite3.connect(db_path)
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            response TEXT,
            timestamp DATETIME
        )
        ''')
        self.conn.commit()
        
        # Load history
        self.load_history()
    
    def init_tts(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.8)
        
        # Get available voices
        voices = self.engine.getProperty('voices')
        # Try to set a Russian voice if available
        for voice in voices:
            if 'russian' in voice.name.lower() or 'ru' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
    
    def init_audio(self):
        try:
            pygame.mixer.init()
            # Check if ambient music file exists, if not, we'll skip playing music
            music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ambient.mp3')
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)  # Loop indefinitely
        except Exception as e:
            print(f"Не удалось инициализировать аудио: {str(e)}")
    
    def show_welcome_message(self):
        welcome_msg = "Добро пожаловать в ИКАР-Ассистент! Чем я могу помочь вам сегодня?"
        self.results_text.setText(welcome_msg)
        
        # Speak welcome message in a separate thread to avoid UI freezing
        threading.Thread(target=self.speak_text, args=(welcome_msg,), daemon=True).start()
    
    def search(self):
        query = self.input_text.toPlainText().strip()
        if not query:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, введите запрос")
            return
        
        # Show loading message
        self.results_text.setText("Поиск решения, пожалуйста подождите...")
        self.search_button.setEnabled(False)
        
        # Clear previous links
        self.links_list.clear()
        self.current_links = []
        
        # Start search in a separate thread
        self.search_worker = SearchWorker(query)
        self.search_worker.finished.connect(self.handle_search_results)
        self.search_worker.start()
    
    def handle_search_results(self, ai_response, search_results):
        # Format the response
        full_response = ai_response + "\n\n"
        
        # Add search results
        if search_results:
            full_response += "Дополнительные источники информации:\n"
            for i, result in enumerate(search_results, 1):
                full_response += f"{i}. {result['title']}\n"
                self.current_links.append(result['url'])
                
                # Add to links list
                item = QListWidgetItem(f"{i}. {result['title']}")
                item.setToolTip(result['snippet'])
                self.links_list.addItem(item)
        else:
            full_response += "Не удалось найти дополнительные источники информации."
        
        # Display results
        self.results_text.setText(full_response)
        
        # Save to history
        self.save_to_history(self.input_text.toPlainText(), full_response)
        
        # Enable buttons
        self.search_button.setEnabled(True)
        self.speak_button.setEnabled(True)
        self.open_link_button.setEnabled(len(self.current_links) > 0)
    
    def speak_response(self):
        text = self.results_text.toPlainText()
        if text:
            # Speak in a separate thread to avoid UI freezing
            threading.Thread(target=self.speak_text, args=(text,), daemon=True).start()
    
    def speak_text(self, text):
        try:
            self.engine.stop()  # Stop any current speech
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Ошибка при озвучивании текста: {str(e)}")
    
    def open_link(self):
        selected_items = self.links_list.selectedItems()
        if selected_items:
            index = self.links_list.row(selected_items[0])
            if 0 <= index < len(self.current_links):
                url = self.current_links[index]
                # Open URL in default browser
                import webbrowser
                webbrowser.open(url)
        else:
            QMessageBox.information(self, "Информация", "Пожалуйста, выберите ссылку из списка")
    
    def select_link(self):
        self.open_link_button.setEnabled(True)
    
    def save_to_history(self, query, response):
        cursor = self.conn.cursor()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO history (query, response, timestamp) VALUES (?, ?, ?)",
                      (query, response, timestamp))
        self.conn.commit()
        
        # Update history list
        self.load_history()
    
    def load_history(self):
        self.history_list.clear()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, query, timestamp FROM history ORDER BY timestamp DESC LIMIT 50")
        for row in cursor.fetchall():
            item = QListWidgetItem(f"{row[2]} - {row[1][:30]}...")
            item.setData(Qt.UserRole, row[0])  # Store history ID
            self.history_list.addItem(item)
    
    def load_history_item(self):
        selected_items = self.history_list.selectedItems()
        if selected_items:
            history_id = selected_items[0].data(Qt.UserRole)
            cursor = self.conn.cursor()
            cursor.execute("SELECT query, response FROM history WHERE id = ?", (history_id,))
            result = cursor.fetchone()
            if result:
                self.input_text.setText(result[0])
                self.results_text.setText(result[1])
                self.speak_button.setEnabled(True)
    
    def closeEvent(self, event):
        # Stop audio and close database connection
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        
        if hasattr(self, 'conn'):
            self.conn.close()
        
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IkarAssistant()
    window.show()
    sys.exit(app.exec_())