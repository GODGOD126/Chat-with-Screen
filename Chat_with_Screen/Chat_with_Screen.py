import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageFilter,ImageChops,ImageGrab
import requests
import base64
from io import BytesIO
import threading
import datetime
import ctypes

# OpenAI API Key
api_key = ""



# Function to encode the image
def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')



def create_round_button_image(image_path, output_size):
    # Load the image in RGBA mode
    image = Image.open(image_path).convert("RGBA")

    # Resize the image to fit the output size with high-quality resampling
    image = image.resize((output_size, output_size), Image.LANCZOS)

    # Create a mask for the circular area
    mask = Image.new('L', (output_size, output_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, output_size, output_size), fill=255)

    # Apply the mask to the image to get a round button
    round_image = Image.new('RGBA', (output_size, output_size), (0, 0, 0, 0))
    round_image.paste(image, (0, 0), mask=mask)

    return round_image

def create_round_window(root, image_path):
    output_size = 400  # Increase the diameter size of the button

    # Create the round button image
    round_image = create_round_button_image(image_path, output_size)

    # Convert the PIL image to a format that Tkinter can use
    photo = ImageTk.PhotoImage(round_image)

    # Configure the Tkinter window
    root.overrideredirect(True)  # Remove the window border and title bar
    root.wm_attributes("-topmost", True)  # Keep the window on top
    root.attributes("-transparentcolor", "black")  # Set window to be transparent

    # Set the window size to match the round image
    root.geometry(f"{output_size}x{output_size}+100+100")  # Set the position

    # Use a label to display the round image
    label = tk.Label(root, image=photo, bg='black')
    label.image = photo  # Keep a reference to the image
    label.pack()
    
    right_click_menu = tk.Menu(root, tearoff=0)
    right_click_menu.add_command(label="QUIT", command=root.quit)
    
    def on_right_click(event):
        right_click_menu.post(event.x_root, event.y_root)

    # drag window
    def on_drag(event):
        x = root.winfo_pointerx() - offset_x
        y = root.winfo_pointery() - offset_y
        root.geometry(f"+{x}+{y}")

   
    def on_click(event):
    # 单击效果 - 临时放大图像
        temp_output_size = output_size + 10
        clicked_image = create_round_button_image(image_path, temp_output_size)
        clicked_photo = ImageTk.PhotoImage(clicked_image)
        label.config(image=clicked_photo)
        label.image = clicked_photo  # Keep a reference to avoid garbage collection
        # Scale back to original size after a short delay
        root.after(100, lambda: label.config(image=photo))
        
        # 拖拽效果 - 初始化位置
        global offset_x, offset_y
        offset_x = event.x
        offset_y = event.y

    def on_double_click(event):
        toggle_chat_window()
        # 双击效果 - 检查并恢复最小化的聊天窗口
        global chat_window
        if 'chat_window' in globals() and chat_window is not None:
            # 如果窗口最小化，则先恢复窗口
            if chat_window.state() == 'iconic':
                chat_window.deiconify()
            # 不管窗口是否最小化，都将其置顶
            chat_window.lift()
            chat_window.focus()  # 聚焦到窗口
        # 绑定事件处理函数到 label
    label.bind("<Button-1>", on_click)  # 单击事件
    label.bind("<Double-Button-1>", on_double_click)  # 双击事件
    label.bind("<B1-Motion>", on_drag)  # 拖动事件
    label.bind("<Button-3>", on_right_click)

    # 用于保持对点击事件处理函数的引用，防止被垃圾回收
    root.on_click = on_click
def toggle_chat_window():
    global chat_window
    if chat_window is None or not chat_window.winfo_exists():
        create_chat_window()
    # 如果窗口已经存在，不执行任何操作
def create_chat_window():
    global chat_window, user_text, gpt_text, input_entry
    chat_window = tk.Toplevel()
    chat_window.title("Chat with Screenshot")

    # 主框架，用于放置文本框和输入框
    main_frame = tk.Frame(chat_window)
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # GPT反馈窗口的滚动条
    scrollbar_gpt = tk.Scrollbar(main_frame)
    scrollbar_gpt.pack(side=tk.LEFT, fill=tk.Y)

    # 用户信息窗口的滚动条
    scrollbar_user = tk.Scrollbar(main_frame)
    scrollbar_user.pack(side=tk.RIGHT, fill=tk.Y)

    # 创建文本框用于显示GPT的反馈
    gpt_text = tk.Text(main_frame, height=15, width=25, bg="white", state=tk.DISABLED, yscrollcommand=scrollbar_gpt.set)
    gpt_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_gpt.config(command=gpt_text.yview)

    # 创建文本框用于显示用户的输入内容
    user_text = tk.Text(main_frame, height=15, width=25, bg="lightgrey", state=tk.DISABLED, yscrollcommand=scrollbar_user.set)
    user_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_user.config(command=user_text.yview)

    # 创建输入框和截屏发送按钮
    input_frame = tk.Frame(chat_window)
    input_frame.pack(side=tk.BOTTOM, fill=tk.X)
    input_entry = tk.Entry(input_frame)
    input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    send_screenshot_button = tk.Button(input_frame, text="Screenshot+Send", command=send_screenshot_message)
    send_screenshot_button.pack(side=tk.RIGHT)

    input_entry.bind("<Return>", lambda event: send_screenshot_message())

    fill_chat_history()

    # 更新窗口尺寸
    chat_window.update_idletasks()
    current_width = chat_window.winfo_width()
    current_height = chat_window.winfo_height()
    new_width = int(current_width * 1.3)
    new_height = int(current_height * 1.6)
    chat_window.geometry(f"{new_width}x{new_height}")


def fill_chat_history():
    # 使用聊天历史记录填充聊天窗口
    user_text.config(state=tk.NORMAL)
    gpt_text.config(state=tk.NORMAL)
    user_text.delete(1.0, tk.END)
    gpt_text.delete(1.0, tk.END)
    for message in chat_history:
        if message['sender'] == 'user':
            user_text.insert(tk.END, message['text'] + "\n")
        else:
            gpt_text.insert(tk.END, message['text'] + "\n")
    user_text.config(state=tk.DISABLED)
    gpt_text.config(state=tk.DISABLED)

def send_text_message():
    message = input_entry.get()
    if message:
        add_message_to_history('user', message)
        input_entry.delete(0, tk.END)
        
        # 这里可以添加将文本消息发送到GPT-4的代码，并获取回复
        gpt_response = "GPT Response"

        add_message_to_history('gpt', gpt_response)

def send_screenshot_message():
    # 显示处理中提示
    add_message_to_history('gpt', 'loading...')
    threading.Thread(target=process_screenshot_message).start()

def process_screenshot_message():
    global chat_history
    message = input_entry.get()

    # 先隐藏聊天窗口
    chat_window.withdraw()

    # 短暂等待确保窗口已经隐藏
    chat_window.update_idletasks()
    chat_window.after(500)  # 暂停500毫秒

    # 截取屏幕并编码
    screenshot = ImageGrab.grab()
    base64_image = encode_image(screenshot)

    # 恢复显示聊天窗口
    chat_window.deiconify()

    # 如果有文本消息，添加到历史记录中
    if message:
        add_message_to_history('user', message)
        input_entry.delete(0, tk.END)

    # 构造请求头和载荷
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }

    # 发送请求
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        gpt_response = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
        add_message_to_history('gpt', gpt_response)
    else:
        add_message_to_history('gpt', "Error in API response")

    fill_chat_history()


def add_message_to_history(sender, text):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sender_tag = "[GPT]" if sender == 'gpt' else "[User]"

    formatted_message = f"{current_time} {sender_tag}\n{text}\n\n"

    chat_history.append({'sender': sender, 'text': formatted_message})

    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(formatted_message)

    fill_chat_history()


def fill_chat_history():
    user_text.config(state=tk.NORMAL)
    gpt_text.config(state=tk.NORMAL)
    user_text.delete(1.0, tk.END)
    gpt_text.delete(1.0, tk.END)

    for message in chat_history:
        if message['sender'] == 'user':
            user_text.insert(tk.END, message['text'] + "\n\n")  # 添加额外的换行符
        else:
            gpt_text.insert(tk.END, message['text'] + "\n\n")  # 添加额外的换行符
    # 滚动到底部
    user_text.see("end")
    gpt_text.see("end")
    user_text.config(state=tk.DISABLED)
    gpt_text.config(state=tk.DISABLED)
    
chat_history = []
    
def load_chat_history():
    global chat_history
    try:
        with open("chat_history.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        

        message_buffer = []
        for line in lines:
            if line.strip():  # 如果行不是空的
                message_buffer.append(line.strip())
            else:
                # 当遇到空行时，处理当前消息
                if message_buffer:
                    # 提取发送者
                    sender = 'gpt' if message_buffer[0].endswith("[GPT]") else 'user'
                    # 合并消息文本
                    text = " ".join(message_buffer[1:])  # 剩余行是消息文本
                    chat_history.append({'sender': sender, 'text': text})
                    
                    message_buffer.clear()

    except FileNotFoundError:
        print("File not found")  # 如果文件不存在，则打印提示





try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except (AttributeError, OSError):
    pass  # This modification is only relevant on Windows

# 创建Tkinter窗口
root = tk.Tk()

# 加载聊天历史
load_chat_history()

create_round_window(root, "test.png")

# 初始化聊天窗口和聊天历史记录变量
chat_window = None
user_text = None
gpt_text = None
input_entry = None
# chat_history = []  # 此行应该被注释掉或删除，以避免覆盖已加载的聊天记录

# 运行Tkinter事件循环
root.mainloop()
