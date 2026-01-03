import cv2
import os

# -----------------------------
# FILE PATHS
# -----------------------------
IMAGE_FLD = "images"          # Input image
LABEL_FLD = "labels"       # Output label file

img_name = '02.jpg'
label_name = 'label.txt'

img_path = os.path.join(IMAGE_FLD, img_name)

# -----------------------------
# GLOBAL VARIABLES
# -----------------------------Q
boxes = []                     # Stores all drawn bounding boxes (x1,y1,x2,y2)
drawing = False                # Mouse state flag
start_x, start_y = -1, -1      # Starting point of rectangle

# -----------------------------
# LOAD & PREPARE IMAGE
# -----------------------------
org_img = cv2.imread(img_path)       # Load image
org_img = cv2.resize(org_img, (720, 480))  # Resize for consistent GUI size

img = org_img.copy()            # Permanent image (stores final rectangles)
temp_img = img.copy()           # Temporary display image (for live drawing)

# ============================================================
# FUNCTION: Redraw all saved boxes on the original image
# ============================================================
def recreate_box():
    global img, temp_img, boxes
    img = org_img.copy()        # Reset to original clear image

    # Draw all saved boxes one-by-one
    for x1, y1, x2, y2 in boxes:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    temp_img = img.copy()       # Copy for live preview


# ============================================================
# FUNCTION: Save boxes to a text file
# ============================================================
def save_boxes():
    global LABEL_PATH, boxes, IMAGE_PATH
    path = f'{LABEL_FLD}/{img_name}{label_name}'     # Create output file path

    with open(path, "w") as f:
        for (x1, y1, x2, y2) in boxes:
            f.write(f"0 {x1} {y1} {x2} {y2}\n")   # Write class + coords


# ============================================================
# MOUSE EVENT CALLBACK
# ============================================================
def mouse_callback(event, x, y, flags, params):
    global img, temp_img, boxes, drawing, start_x, start_y

    # -----------------------------
    # Left mouse button pressed → start drawing
    # -----------------------------
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y   # Save starting coords

    # -----------------------------
    # Mouse is moving AND drawing is active → show temp rectangle
    # -----------------------------
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        temp_img = img.copy()     # Refresh background
        cv2.rectangle(temp_img, (start_x, start_y), (x, y), (0, 0, 255), 2)

    # -----------------------------
    # Left mouse button released → final rectangle
    # -----------------------------
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_x, end_y = x, y       # Save end coords

        # Sort coordinates so x1 < x2 and y1 < y2
        x1, y1 = min(start_x, end_x), min(start_y, end_y)
        x2, y2 = max(start_x, end_x), max(start_y, end_y)

        boxes.append((x1, y1, x2, y2))   # Add box to list

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw permanent box
        temp_img = img.copy()        # Refresh preview image


# ============================================================
# SETUP WINDOW & CALLBACK
# ============================================================
cv2.namedWindow("Label")
cv2.setMouseCallback("Label", mouse_callback)

# ============================================================
# MAIN LOOP
# ============================================================
while True:
    cv2.imshow("Label", temp_img)     # Always show temp image

    key = cv2.waitKey(1)

    if key == ord('q'):        # Quit program
        break

    elif key == ord('z'):      # Undo last box
        if boxes:
            boxes.pop()
            recreate_box()

    elif key == ord('s'):      # Save boxes to text file
        save_boxes()

cv2.destroyAllWindows()
