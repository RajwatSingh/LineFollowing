# PiCar-X Line-Following Intersection Navigator

A Python program for the [PiCar-X robotic chassis](https://github.com/Elecrow-CrowPi/PiCar-X) that follows a line, handles intersections, and chooses exits at random.  

---

## 📦 Features

- **Line Following**  
  - Gentle corrections when slightly off‐line  
  - Sharper recovery turns when more drastically off‐line  
- **Intersection Detection & Handling**  
  - Detects junctions by counting consecutive sensor triggers  
  - Backs up slightly, then randomly chooses “straight”, “left” or “right” exit  
- **Configurable Parameters**  
  - Grayscale thresholds for sensors  
  - Motor speeds for forward/backward  
  - Servo angles for corrections and sharp turns  
  - Intersection confirmation threshold  
- **Safe Shutdown**  
  - Gracefully stops motors on program exit (e.g. Ctrl+C)

---

## 🛠️ Prerequisites

- **Hardware**  
  - PiCar-X robotic chassis  
  - Raspberry Pi (3B+ or newer recommended)  
  - 3-sensor line follower module  
- **Software**  
  - Python 3.7+  
  - `picarx` library  
  - `robot_hat` library (for servos)  

---

## 🚀 Installation

1. **Clone this repository**  
   ```bash
   git clone https://github.com/yourusername/PiCarX-LineFollower.git
   cd PiCarX-LineFollower