import cv2
import mediapipe as mp

def main():
    cap = cv2.VideoCapture(0)
    # Set input resolution
    cap.set(3, 1280)
    cap.set(4, 720)
    print(cap.get(3), cap.get(4))

    # Camera loop
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read frame")
            break

        img = cv2.flip(img, 1)
        cv2.imshow("image", img)

        # Update window, check for exit key q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()