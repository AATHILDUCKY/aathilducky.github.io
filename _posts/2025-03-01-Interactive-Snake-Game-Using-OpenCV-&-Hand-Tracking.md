---
title: Interactive Snake Game Using OpenCV & Hand Tracking
categories: projects
tags: ['opencv']
---




## 🚀 Interactive Snake Game Using OpenCV & Hand Tracking in Python

### Introduction

Are you looking for a fun, interactive project using Python, OpenCV, and Hand Tracking? In this guide, you'll learn how to build an interactive Snake Game controlled with your fingers using MediaPipe Hand Tracking and OpenCV.

This project is perfect for beginners and intermediate programmers interested in computer vision, game development, and artificial intelligence. Let's dive into the code and explore how to create a gesture-controlled Snake Game from scratch!


### Features of the Interactive Snake Game

✅ Hand-Tracking Control – Move the snake using your index finger.
✅ Real-time Interaction – The snake follows your hand movements dynamically.
✅ Food Collection & Score System – Eat food to grow the snake and increase the score.
✅ Collision Detection – Game over when the snake touches the border or itself.
✅ Restart & Quit Functionality – Restart with the 'R' key and quit with 'Q'.


### Technologies Used
- Python – Programming language for game logic and computer vision.
- OpenCV – For capturing video from the webcam and rendering graphics.
- MediaPipe – For real-time hand-tracking detection.
- NumPy – For handling mathematical operations efficiently.

### Prerequisites
Before you start, ensure you have the following installed:
```bash
pip install opencv-python mediapipe numpy
```

### Code for Hand-Controlled Snake Game
```python
import cv2
import mediapipe as mp
import numpy as np
import random

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Game Window Size
width, height = 800, 600

# Game Variables
snake_size = 10
speed = 5

def reset_game():
    global snake_pos, snake_length, food_pos, score, game_over
    snake_pos = [(width // 2, height // 2)]  # Snake starting position
    snake_length = 5
    food_pos = (random.randint(50, width - 50), random.randint(50, height - 50))
    score = 0
    game_over = False

# Initialize game
reset_game()

# Open Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (width, height))

    # Convert to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    finger_position = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the tip of the index finger
            index_finger = hand_landmarks.landmark[8]
            finger_position = (int(index_finger.x * width), int(index_finger.y * height))

    # Move Snake Towards Finger
    if not game_over and finger_position:
        snake_x, snake_y = snake_pos[-1]  # Get last position (snake head)
        finger_x, finger_y = finger_position

        # Calculate movement direction
        dx, dy = finger_x - snake_x, finger_y - snake_y
        dist = np.sqrt(dx ** 2 + dy ** 2)

        if dist > 0:
            move_x = int((dx / dist) * speed)
            move_y = int((dy / dist) * speed)
        else:
            move_x, move_y = 0, 0

        new_head = (snake_x + move_x, snake_y + move_y)
        snake_pos.append(new_head)

        # Keep snake length fixed
        if len(snake_pos) > snake_length:
            snake_pos.pop(0)

        # Check if Snake Eats Food
        head_x, head_y = snake_pos[-1]
        food_x, food_y = food_pos

        if abs(head_x - food_x) < 15 and abs(head_y - food_y) < 15:  # Collision check
            snake_length += 5  # Increase size
            score += 10  # Increase score
            food_pos = (random.randint(50, width - 50), random.randint(50, height - 50))  # New food position

        # Check for Border Collision
        if head_x <= 0 or head_x >= width or head_y <= 0 or head_y >= height:
            game_over = True

        # Check for Self Collision
        if new_head in snake_pos[:-1]:  # If the head touches its body
            game_over = True

    # Draw Snake
    for i, pos in enumerate(snake_pos):
        color = (0, 255 - i * 5, 0)  # Gradual green effect
        cv2.circle(frame, pos, snake_size, color, -1)

    # Draw Food
    cv2.circle(frame, food_pos, 8, (0, 0, 255), -1)  # Red food

    # Display Score
    cv2.putText(frame, f"Score: {score}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show Game Over Message
    if game_over:
        cv2.putText(frame, "GAME OVER", (width // 3, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        cv2.putText(frame, "Press 'R' to Restart", (width // 3, height // 2 + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show Game Window
    cv2.imshow("Snake Game - Finger Control", frame)

    # Check for Quit ('q') or Restart ('r')
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r') and game_over:
        reset_game()  # Restart the game

cap.release()
cv2.destroyAllWindows()

```

### How the Code Works

- 🎯 Step 1: Initialize Hand Tracking
Uses MediaPipe Hands to detect and track hand movements.
Captures the index finger's position to control the snake.
- 🎯 Step 2: Control Snake Movement
The snake follows the detected finger's position dynamically.
Moves in the direction of the finger's location on the screen.
- 🎯 Step 3: Detect Food & Increase Score
The snake eats food when its head touches the food position.
The score increases by 10, and the snake grows in length.
- 🎯 Step 4: Collision Detection
If the snake touches the border or its own body, the game ends.
Displays a GAME OVER message with an option to restart.

### Final Thoughts
This interactive Snake Game using OpenCV and Hand Tracking is a great project to learn real-time hand gesture recognition. It integrates computer vision with game development, making it an exciting project for Python enthusiasts.

### 🔥 What’s Next?
- ✅ Add more gestures – Use different fingers to control speed or change direction.
- ✅ Enhance the UI – Add animations and a graphical interface.
- ✅ Implement AI – Use AI models to predict better movement patterns.

Start coding today and create your own gesture-controlled Snake Game! 🎮🐍




<iframe src="https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7301191485511606272" height="900" width="504" frameborder="0" allowfullscreen="" title="Embedded post"></iframe>