# استفاده از تصویر پایتون رسمی به عنوان پایه
FROM python

# تنظیم محل کار در کانتینر
WORKDIR /app

# کپی فایل‌های مورد نیاز برای نصب وابستگی‌ها
COPY requirements.txt /app/

# نصب وابستگی‌های پروژه
RUN pip install --no-cache-dir -r requirements.txt

# کپی سایر فایل‌ها به کانتینر
COPY . /app/
