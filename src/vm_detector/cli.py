import sys
from vm_detector import create_detector


def main():
    try:
        detector = create_detector()
        detector.detect()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
