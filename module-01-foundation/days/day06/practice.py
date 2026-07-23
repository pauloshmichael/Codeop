# ============================================
#  Spot the SRP Violation
# Split a Report class that builds, saves, and emails a report
# ============================================

class ReportData:
    """Responsibility: Store and manage report data"""
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author
        self.date = "2026-07-23"
    
    def get_formatted_data(self):
        return f"Report: {self.title}\nDate: {self.date}\nAuthor: {self.author}\n\n{self.content}"


class ReportBuilder:
    """Responsibility: Build and format the report"""
    def __init__(self, report_data):
        self.report_data = report_data
    
    def build_report(self):
        return self.report_data.get_formatted_data()
    
    def build_html_report(self):
        data = self.report_data
        return f"""
        <html>
            <head><title>{data.title}</title></head>
            <body>
                <h1>{data.title}</h1>
                <p><strong>Date:</strong> {data.date}</p>
                <p><strong>Author:</strong> {data.author}</p>
                <p>{data.content}</p>
            </body>
        </html>
        """


class ReportSaver:
    """Responsibility: Save the report to different storage locations"""
    def __init__(self, report_builder):
        self.report_builder = report_builder
    
    def save_to_file(self, filename):
        content = self.report_builder.build_report()
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Report saved to {filename}")
    
    def save_to_database(self):
        # Simulate database save
        print("Report saved to database")


class ReportEmailer:
    """Responsibility: Handle email sending"""
    def __init__(self, report_builder):
        self.report_builder = report_builder
    
    def send_email(self, recipient, subject):
        content = self.report_builder.build_report()
        print(f"Email sent to {recipient}")
        print(f"Subject: {subject}")
        print(f"Content: {content[:100]}...")
        print("Email sent successfully!")


# Test Exercise 1
def test_exercise1():
    print("\n" + "="*60)
    print("EXERCISE 1: SRP Violation Refactored")
    print("="*60)
    
    # Create report data
    report_data = ReportData(
        title="Monthly Sales Report",
        content="Total sales for June: 1,000,000 ETB. Growth: 15%.",
        author="John Doe"
    )
    
    # Build the report
    builder = ReportBuilder(report_data)
    
    # Save the report
    saver = ReportSaver(builder)
    saver.save_to_file("monthly_report.txt")
    saver.save_to_database()
    
    # Email the report
    emailer = ReportEmailer(builder)
    emailer.send_email("manager@company.com", "Monthly Sales Report")


# ============================================
#  Refactor to OCP
# Replace if/elif with class hierarchy
# ============================================

from abc import ABC, abstractmethod
import math

class Shape(ABC):
    """Abstract base class for all shapes"""
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def name(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def name(self):
        return "Circle"


class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side ** 2
    
    def name(self):
        return "Square"


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height
    
    def area(self):
        return 0.5 * self.base * self.height
    
    def name(self):
        return "Triangle"


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def name(self):
        return "Rectangle"


def print_area_ocp(shape):
    """OCP-compliant function - works with any new shape without modification"""
    print(f"{shape.name()} area: {shape.area():.2f}")


def test_exercise2():
    print("\n" + "="*60)
    print("EXERCISE 2: OCP Refactored")
    print("="*60)
    
    shapes = [
        Circle(5),
        Square(4),
        Triangle(3, 6),
        Rectangle(4, 5)  # New shape added without modifying existing code
    ]
    
    for shape in shapes:
        print_area_ocp(shape)


# ============================================
# Write a Singleton
# AppSettings Singleton holding currency
# ============================================

class AppSettings:
    """Singleton class for application settings"""
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppSettings, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not AppSettings._initialized:
            self.currency = "ETB"
            self.app_name = "TeleBirr System"
            self.version = "1.0"
            AppSettings._initialized = True
    
    def set_currency(self, currency):
        self.currency = currency
    
    def get_settings(self):
        return {
            "currency": self.currency,
            "app_name": self.app_name,
            "version": self.version
        }


def test_exercise3():
    print("\n" + "="*60)
    print("EXERCISE 3: Singleton Pattern")
    print("="*60)
    
    # Create two instances
    settings1 = AppSettings()
    settings2 = AppSettings()
    
    # Check if they're the same object
    print(f"settings1 is settings2: {settings1 is settings2}")
    print(f"ID of settings1: {id(settings1)}")
    print(f"ID of settings2: {id(settings2)}")
    
    # Show initial settings
    print(f"\nInitial settings: {settings1.get_settings()}")
    
    # Change currency using settings1
    settings1.set_currency("USD")
    print(f"Changed currency to USD using settings1")
    
    # Check using settings2 (should reflect the change)
    print(f"Settings from settings2: {settings2.get_settings()}")
    
    # Both instances are the same object
    print(f"\nsettings1.currency: {settings1.currency}")
    print(f"settings2.currency: {settings2.currency}")
    print(f"settings1 is settings2: {settings1 is settings2}")


# ============================================
# Write a Factory
# ShapeFactory that creates Circle, Square, Triangle
# ============================================

class ShapeFactory:
    """Factory class to create different shapes"""
    
    @staticmethod
    def create(kind, *args, **kwargs):
        """
        Create a shape based on the kind parameter
        
        Args:
            kind: Type of shape ('circle', 'square', 'triangle', 'rectangle')
            *args, **kwargs: Shape-specific parameters
        
        Returns:
            Shape object or None if invalid kind
        """
        kind = kind.lower()
        
        if kind == "circle":
            if 'radius' in kwargs:
                return Circle(kwargs['radius'])
            elif len(args) >= 1:
                return Circle(args[0])
            else:
                raise ValueError("Circle requires 'radius' parameter")
        
        elif kind == "square":
            if 'side' in kwargs:
                return Square(kwargs['side'])
            elif len(args) >= 1:
                return Square(args[0])
            else:
                raise ValueError("Square requires 'side' parameter")
        
        elif kind == "triangle":
            if 'base' in kwargs and 'height' in kwargs:
                return Triangle(kwargs['base'], kwargs['height'])
            elif len(args) >= 2:
                return Triangle(args[0], args[1])
            else:
                raise ValueError("Triangle requires 'base' and 'height' parameters")
        
        elif kind == "rectangle":
            if 'width' in kwargs and 'height' in kwargs:
                return Rectangle(kwargs['width'], kwargs['height'])
            elif len(args) >= 2:
                return Rectangle(args[0], args[1])
            else:
                raise ValueError("Rectangle requires 'width' and 'height' parameters")
        
        else:
            return None  # Invalid shape kind

def test_exercise4():
    print("\n" + "="*60)
    print("EXERCISE 4: Factory Pattern")
    print("="*60)
    
    # Create shapes using the factory
    shapes = [
        ShapeFactory.create("circle", radius=5),
        ShapeFactory.create("square", side=4),
        ShapeFactory.create("triangle", base=3, height=6),
        ShapeFactory.create("rectangle", width=4, height=5),
    ]
    
    # Try to create an invalid shape
    invalid_shape = ShapeFactory.create("hexagon")
    if invalid_shape is None:
        print("Invalid shape type: 'hexagon' not supported")
    print()
    
    # Display areas
    for shape in shapes:
        print_area_ocp(shape)


# ============================================
#  Write an Observer pair
# NewsAgency subject with subscribers
# ============================================

class Subscriber:
    """Abstract base class for subscribers"""
    def update(self, news):
        pass


class NewsAgency:
    """Subject class that maintains list of observers/subscribers"""
    def __init__(self):
        self.subscribers = []
        self.latest_news = ""
    
    def subscribe(self, subscriber):
        """Add a subscriber to the list"""
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
            print(f"Subscriber {subscriber.__class__.__name__} subscribed successfully")
    
    def unsubscribe(self, subscriber):
        """Remove a subscriber from the list"""
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
            print(f"Subscriber {subscriber.__class__.__name__} unsubscribed successfully")
    
    def publish_news(self, news):
        """Publish news and notify all subscribers"""
        self.latest_news = news
        print(f"\n📢 News Agency: Publishing '{news}'")
        self.notify_subscribers()
    
    def notify_subscribers(self):
        """Notify all subscribers with the latest news"""
        for subscriber in self.subscribers:
            subscriber.update(self.latest_news)


class EmailSubscriber(Subscriber):
    """Email subscriber that receives news via email"""
    def __init__(self, email):
        self.email = email
    
    def update(self, news):
        print(f"📧 Email sent to {self.email}: {news}")
        print(f"   (Simulated email delivery)")


class SMSSubscriber(Subscriber):
    """SMS subscriber that receives news via text message"""
    def __init__(self, phone_number):
        self.phone_number = phone_number
    
    def update(self, news):
        print(f"📱 SMS sent to {self.phone_number}: {news}")
        print(f"   (Simulated SMS delivery)")


class PushNotificationSubscriber(Subscriber):
    """Push notification subscriber"""
    def __init__(self, device_id):
        self.device_id = device_id
    
    def update(self, news):
        print(f"🔔 Push notification sent to device {self.device_id}: {news}")
        print(f"   (Simulated push notification)")


class LoggerSubscriber(Subscriber):
    """Logger subscriber that logs all news"""
    def update(self, news):
        print(f"📝 Logged news: {news}")
        print(f"   (Simulated logging)")


def test_exercise5():
    print("\n" + "="*60)
    print("EXERCISE 5: Observer Pattern")
    print("="*60)
    
    # Create the news agency (subject)
    news_agency = NewsAgency()
    
    # Create subscribers
    email_sub = EmailSubscriber("user@example.com")
    sms_sub = SMSSubscriber("+251-900-000-000")
    push_sub = PushNotificationSubscriber("device-1234")
    logger_sub = LoggerSubscriber()
    
    # Subscribe all observers
    print("\n=== Subscribing subscribers ===")
    news_agency.subscribe(email_sub)
    news_agency.subscribe(sms_sub)
    news_agency.subscribe(push_sub)
    news_agency.subscribe(logger_sub)
    
    # Publish first news
    news_agency.publish_news("TeleBirr launches new premium features!")
    
    # Unsubscribe SMS subscriber
    print("\n=== Unsubscribing SMS subscriber ===")
    news_agency.unsubscribe(sms_sub)
    
    # Publish second news
    news_agency.publish_news("TeleBirr announces 5% cashback on all transactions!")
    
    # Subscribe a new subscriber
    print("\n=== Adding new subscriber ===")
    new_email_sub = EmailSubscriber("newuser@company.com")
    news_agency.subscribe(new_email_sub)
    
    # Publish third news
    news_agency.publish_news("TeleBirr partners with major banks for integration!")
    
    print("\n" + "="*60)
    print("All exercises completed!")
    print("="*60)


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("DAY 6 - SOLID Principles & Design Patterns Exercises")
    print("="*60)
    
    # Run all exercise tests
    test_exercise1()
    test_exercise2()
    test_exercise3()
    test_exercise4()
    test_exercise5()
    
    print("\n" + "="*60)
    print("🎉 All tests completed successfully!")
    print("="*60)