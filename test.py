import time

def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(i)
        time.sleep(1)

# นับถอยหลังจาก 5 วินาที
countdown_timer(5)

print("หลังจากนับถอยหลังเสร็จแล้ว!")
