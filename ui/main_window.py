from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTextEdit
)

from models.post_request import PostRequest
from services.marketing_service import MarketingService


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("AI Marketing Studio")

        self.resize(700, 500)

        self.marketing_service = MarketingService()

        layout = QVBoxLayout()

        title = QLabel("AI Marketing Studio")

        business = QLabel("Business")

        business_name = QLabel("Umiya Trading Company")

        post_type_label = QLabel("Post Type")

        self.post_type = QComboBox()

        self.post_type.addItems([
            "Educational",
            "Advertisement",
            "Product Showcase",
            "Comparison",
            "Offer",
            "Tips & Tricks",
            "Festival",
            "Customer Testimonial",
            "Myth vs Fact"
        ])

        topic = QLabel("Today's Topic")

        self.topic_input = QLineEdit()

        self.topic_input.setPlaceholderText(
            "Example: Why BWP plywood is best for kitchens"
        )

        generate = QPushButton("Generate Prompt")

        generate.clicked.connect(self.generate_post)

        self.status = QLabel("Ready")

        layout.addWidget(title)
        layout.addSpacing(20)

        layout.addWidget(business)
        layout.addWidget(business_name)

        layout.addSpacing(20)

        layout.addWidget(post_type_label)
        layout.addWidget(self.post_type)

        layout.addSpacing(20)

        layout.addWidget(topic)
        layout.addWidget(self.topic_input)

        layout.addSpacing(20)

        layout.addWidget(generate)

        layout.addSpacing(20)

        layout.addWidget(self.status)

        self.setLayout(layout)

        preview_label = QLabel("Generated Prompt")

        self.prompt_preview = QTextEdit()

        self.prompt_preview.setReadOnly(True)

        self.prompt_preview.setPlaceholderText(
            "Your generated prompt will appear here..."
        )

        layout.addSpacing(20)

        layout.addWidget(preview_label)

        layout.addWidget(self.prompt_preview)

        copy_button = QPushButton("Copy Prompt")
        
        open_button = QPushButton("Open ChatGPT")
        
        save_button = QPushButton("Save Prompt")
        
        copy_button.clicked.connect(self.copy_prompt)
        
        open_button.clicked.connect(self.open_chatgpt)
        
        save_button.clicked.connect(self.save_prompt)
        
        layout.addWidget(copy_button)
        layout.addWidget(open_button)
        layout.addWidget(save_button)

    def generate_post(self):

        topic = self.topic_input.text().strip()

        if not topic:

            self.status.setText("Please enter today's topic.")

            return

        request = PostRequest(
            topic=topic,
            post_type=self.post_type.currentText(),
            platform="Instagram"
        )

        prompt = self.marketing_service.generate(request)

        self.prompt_preview.setPlainText(prompt)

        

        self.status.setText(
            "✅ Prompt copied to clipboard."
        )



    def copy_prompt(self):

        self.status.setText("Coming Soon")


    def open_chatgpt(self):

        self.marketing_service.open_chatgpt()

        self.status.setText(
            "ChatGPT opened successfully."
        )


    def save_prompt(self):

        self.status.setText("Coming Soon")