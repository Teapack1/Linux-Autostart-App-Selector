from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import subprocess

class ServiceManagerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.services = ['mediapipe.service', 'sunbox.service', 'classifyii.service', 'home.service']
        self.current_service = None
        self.buttons = {}
        self.custom_labels = {
            'mediapipe.service': 'Handgestures Mediapipe',
            'sunbox.service': 'Sunbox Mirror CTT tuning',
            'classifyii.service': 'Audio Classify-II',
            'home.service': 'Flask Smart Home',   
        }
        self.descriptions = {
            'mediapipe.service': '1) Connect LAN from the 2. port to the Madrix PC.\n 2) Setup IP addres on the Madrix to 10.255.255.1\n 3) Run hangesture-mediapipy madrix setup.\n 4) Scenes changes be gestures.\n 5) Pointer finger changes position of the light spot.',
            'sunbox.service': '1) Get Wifi module for this PC.\n 2) Start Sunbox module board and the LED.\n 3) Setup IP 192.168.0.2 on the Sunbox module.\n 4) Connect to Wifi "mispot", password is "heslo123".\n 5) Press start on the Sunbox module.',
            'classifyii.service': '1) '
        }
        self.main_layout = None
        self.description_layout = None

    def build(self):
        self.root = BoxLayout()  # root is now directly accessible
        self.main_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        self.description_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        self.build_main_menu()
        self.root.add_widget(self.main_layout)  # Add main_layout to root
        return self.root

    def build_main_menu(self):
        # Build main menu
        for service_name in self.services:
            btn_text = self.custom_labels.get(service_name, f'Start {service_name}')
            btn = Button(text=btn_text, font_size='25sp')
            btn.bind(on_press=lambda instance, name=service_name: self.show_description(name))
            self.main_layout.add_widget(btn)
            self.buttons[service_name] = btn

        # Add exit button to main layout
        exit_btn = Button(text='to Linux', font_size='35sp')
        exit_btn.bind(on_press=lambda instance: self.exit_app())
        self.main_layout.add_widget(exit_btn)

    def show_description(self, service_name):
        self.description_layout.clear_widgets()  # Clear previous widgets

        # Service description
        description = self.descriptions.get(service_name, 'No description available.')
        description_label = Label(text=description, font_size='20sp')
        self.description_layout.add_widget(description_label)

        # Start Service Button
        start_btn = Button(text=f"Start {service_name}", size_hint=(1, 0.1), font_size='20sp')
        start_btn.bind(on_press=lambda instance, name=service_name: self.start_service(name))
        self.description_layout.add_widget(start_btn)

        # Back button
        back_btn = Button(text='Back', size_hint=(1, 0.1), font_size='20sp')
        back_btn.bind(on_press=self.show_main_menu)
        self.description_layout.add_widget(back_btn)

        # Switch to description layout
        if self.main_layout in self.root.children:
            self.root.remove_widget(self.main_layout)
        self.root.add_widget(self.description_layout)

    def show_main_menu(self, instance):
        # Switch to main menu layout
        if self.description_layout in self.root.children:
            self.root.remove_widget(self.description_layout)
        if self.main_layout not in self.root.children:
            self.root.add_widget(self.main_layout)

    def start_service(self, service_name, *args):
        # Stop the currently running service
        if self.current_service and self.current_service != service_name:
            print(f"Stopping {self.current_service}...")
            subprocess.run(['sudo', 'systemctl', 'stop', self.current_service], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.buttons[self.current_service].background_color = (1, 1, 1, 1)  # Reset color of the button

        # Start the new service
        print(f"Starting {service_name}...")
        subprocess.run(['sudo', 'systemctl', 'start', service_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.current_service = service_name
        self.buttons[service_name].background_color = (0, 1, 0, 1)  # Change color to indicate running
        self.show_main_menu(None)  # Return to main menu after starting the service

    def exit_app(self, *args):
        # Stop each service
        for service_name in self.services:
            print(f"Stopping {service_name}...")
            subprocess.run(['sudo', 'systemctl', 'stop', service_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.buttons[service_name].background_color = (1, 1, 1, 1)  # Reset color of the button

        # Reset the current service
        self.current_service = None

        # Exit the app
        print("Exiting the Service Manager...")
        App.get_running_app().stop()

if __name__ == '__main__':
    ServiceManagerApp().run()
