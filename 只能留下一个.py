import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QGridLayout, QPushButton, QLabel)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from functools import partial


class WordSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("词语选择器")
        self.setMinimumSize(800, 600)

        # 数据
        self.words = {
            "手机": "外置器官即为一切",
            "电脑": "另一个大脑，人生的伴侣",
            "爷爷": "爷爷那宽大的，厚实的手",
            "奶奶": "慈祥的老人，最好的亲人",
            "自己": "除我之外，再无他物",
            "父亲": "父爱如山，永远的依靠",
            "母亲": "母爱柔似水，伟大的母亲",
            "外公": "严厉却又真诚，指引前行方向",
            "外婆": "温暖的臂弯，可爱的老人",
            "兄弟": "亲兄弟，同进退",
            "姐妹": "好姐妹，齐欢乐",
        }

        # 主界面
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # 1. 在顶部添加规则说明
        self.rule_label = QLabel("规则:选择你要放弃的事物，只能剩下一个")
        self.rule_label.setStyleSheet("font-size: 30px; font-weight: bold; color: #333;")
        self.rule_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.rule_label)

        # 添加垂直间距
        self.main_layout.addSpacing(30)

        # 2. 使用嵌套布局实现按钮居中
        self.center_widget = QWidget()
        self.center_layout = QVBoxLayout(self.center_widget)
        self.center_layout.setAlignment(Qt.AlignCenter)

        # 网格布局用于按钮
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(15)

        # 将网格布局添加到居中布局
        self.center_layout.addLayout(self.grid_layout)

        # 将居中部件添加到主布局
        self.main_layout.addWidget(self.center_widget, 1)  # 使用拉伸因子1

        # 3. 结果标签
        self.final_label = QLabel()
        self.final_label.setAlignment(Qt.AlignCenter)
        self.final_label.setStyleSheet("""
            font-size: 80px; font-weight: bold;color: #FFFFFF;
            background: #000000; padding: 30px;
        """)
        self.final_label.hide()
        self.main_layout.addWidget(self.final_label, 0, Qt.AlignCenter)

        # 4. 解释标签
        self.explanation_label = QLabel()
        self.explanation_label.setAlignment(Qt.AlignCenter)
        self.explanation_label.setStyleSheet("font-size: 30px; color: black; margin-top: 200px;")
        self.main_layout.addWidget(self.explanation_label)

        # 初始化按钮
        self.init_buttons()

    def init_buttons(self):
        """初始化所有按钮"""
        for i, (word, _) in enumerate(self.words.items()):
            btn = QPushButton(word)
            btn.setFixedSize(150, 80)
            btn.setStyleSheet("""
                QPushButton {
                    background: #FFFFFF; border: 2px solid #ddd;
                    border-radius: 8px; font-size: 30px;
                }
                QPushButton:hover { background: #FFFFFF; }
            """)
            btn.clicked.connect(partial(self.on_button_click, word))

            # 计算行列位置（每行最多4个）
            row = i // 4
            col = i % 4
            self.grid_layout.addWidget(btn, row, col, alignment=Qt.AlignCenter)

        # 添加弹性空间使按钮组垂直居中
        self.center_layout.addStretch(1)
        self.main_layout.addStretch(1)

    def on_button_click(self, word):
        """按钮点击处理"""
        # 安全删除按钮
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if widget and widget.text() == word:
                widget.setParent(None)
                widget.deleteLater()
                break

        # 检查剩余按钮
        remaining = [
            self.grid_layout.itemAt(i).widget()
            for i in range(self.grid_layout.count())
            if self.grid_layout.itemAt(i) and self.grid_layout.itemAt(i).widget()
        ]

        if len(remaining) == 1:
            self.show_final_word(remaining[0].text())
        else:
            # 重新排列剩余按钮
            self.rearrange_buttons(remaining)

    def rearrange_buttons(self, buttons):
        """重新排列剩余按钮"""
        # 清除原有按钮
        for i in reversed(range(self.grid_layout.count())):
            if self.grid_layout.itemAt(i).widget():
                self.grid_layout.itemAt(i).widget().setParent(None)

        # 重新添加按钮
        for i, btn in enumerate(buttons):
            row = i // 4
            col = i % 4
            self.grid_layout.addWidget(btn, row, col, alignment=Qt.AlignCenter)

    def show_final_word(self, word):
        """显示最终词语"""
        # 隐藏网格布局
        self.center_widget.hide()

        # 显示最终标签
        self.final_label.setText(word)
        self.final_label.show()

        # 动画效果
        self.animation = QPropertyAnimation(self.final_label, b"geometry")
        self.animation.setDuration(1500)
        self.animation.setEasingCurve(QEasingCurve.OutBounce)

        width, height = 300, 150
        self.animation.setStartValue(QRect(
            (self.width() - width) // 2, -height,
            width, height
        ))
        self.animation.setEndValue(QRect(
            (self.width() - width) // 2, (self.height() - height) // 2,
            width, height
        ))
        self.animation.start()

        # 显示解释
        self.explanation_label.setText(self.words.get(word, ""))
        self.explanation_label.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordSelector()
    window.show()
    sys.exit(app.exec_())
