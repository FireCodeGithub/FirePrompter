import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox

class PrompteurApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prompteur")
        self.root.geometry("600x400")
        
        self.users = {"tout le monde": {}}
        self.scenes = []
        self.current_scene = None
        self.current_user_windows = {}  # To store the text widgets for each user
        self.scene_label = None
        self.config_window = None

        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.start_button.pack(pady=20)
    

    def start(self):
        self.start_button.pack_forget()
        self.open_main_window()
        self.view_config()

    def open_main_window(self):
        self.main_window = tk.Toplevel(self.root)
        self.main_window.title("Main Window")
        self.main_window.geometry("800x600")
        
        self.new_user_button = tk.Button(self.main_window, text="Nouveau Utilisateur", command=self.create_user)
        self.new_user_button.pack(pady=10)
        
        self.new_scene_button = tk.Button(self.main_window, text="Nouvelle Scène", command=self.create_scene)
        self.new_scene_button.pack(pady=10)
        
        self.assign_text_button = tk.Button(self.main_window, text="Assigner Texte", command=self.assign_text)
        self.assign_text_button.pack(pady=10)

        self.finish_button = tk.Button(self.main_window, text="Terminer", command=self.finish_setup)
        self.finish_button.pack(pady=10)
    
    def create_user(self):
        user_name = simpledialog.askstring("Nouveau Utilisateur", "Nom de l'utilisateur:")
        if user_name:
            self.users[user_name] = {}
            for scene in self.scenes:
                self.users[user_name][scene] = ""
            messagebox.showinfo("Info", f"Utilisateur {user_name} créé avec succès.")
            self.refresh_config_window()
    
    def create_scene(self):
        scene_name = simpledialog.askstring("Nouvelle Scène", "Nom de la scène:")
        if scene_name:
            self.scenes.append(scene_name)
            for user in self.users:
                self.users[user][scene_name] = ""
            messagebox.showinfo("Info", f"Scène {scene_name} créée avec succès.")
            self.refresh_config_window()
    
    def assign_text(self):
        assign_window = tk.Toplevel(self.root)
        assign_window.title("Assigner Texte")
        assign_window.geometry("800x600")
        
        for user in self.users:
            user_label = tk.Label(assign_window, text=user)
            user_label.pack()
            
            for scene in self.scenes:
                frame = tk.Frame(assign_window)
                frame.pack(pady=5)
                
                scene_label = tk.Label(frame, text=scene)
                scene_label.pack(side="left")
                
                assign_button = tk.Button(frame, text="Assigner", command=lambda u=user, s=scene: self.load_text(u, s))
                assign_button.pack(side="right")
    
    def load_text(self, user, scene):
        file = filedialog.askopenfile(title="Choisir un fichier texte", filetypes=[("Text files", "*.txt")])
        if file:
            text = file.read()
            file.close()
            self.users[user][scene] = text
            messagebox.showinfo("Info", f"Texte assigné à {user} pour la scène {scene}.")

    def finish_setup(self):
        self.main_window.destroy()
        self.open_navigation_window()
    
    def open_navigation_window(self):
        self.navigation_window = tk.Toplevel(self.root)
        self.navigation_window.title("Navigation")
        self.navigation_window.geometry("800x600")

        self.scene_label = tk.Label(self.navigation_window, text="Scène actuelle: Aucun", font=("Arial", 16))
        self.scene_label.pack(pady=10)

        self.change_scene_button = tk.Button(self.navigation_window, text="Changer de Scène", command=self.change_scene)
        self.change_scene_button.pack(pady=10)

        self.view_user_text_button = tk.Button(self.navigation_window, text="Voir Texte Utilisateur", command=self.view_user_text)
        self.view_user_text_button.pack(pady=10)
    
    def change_scene(self):
        scene_window = tk.Toplevel(self.root)
        scene_window.title("Changer de Scène")
        scene_window.geometry("800x600")
        
        for scene in self.scenes:
            scene_button = tk.Button(scene_window, text=scene, command=lambda s=scene: self.set_current_scene(s))
            scene_button.pack(pady=5)
    
    def set_current_scene(self, scene):
        self.current_scene = scene
        if self.scene_label:
            self.scene_label.config(text=f"Scène actuelle: {scene}")
        self.update_all_text_widgets()
    
    def update_all_text_widgets(self):
        for user, text_widget in self.current_user_windows.items():
            if text_widget and self.current_scene:
                scene_text = self.users[user].get(self.current_scene, "")
                text_widget.config(state="normal")
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", scene_text)
                text_widget.config(state="disabled")
    
    def view_user_text(self):
        user_text_window = tk.Toplevel(self.root)
        user_text_window.title("Texte Utilisateur")
        user_text_window.geometry("800x600")
        
        for user in self.users:
            user_button = tk.Button(user_text_window, text=user, command=lambda u=user: self.display_user_text(u))
            user_button.pack(pady=5)
    
    def display_user_text(self, user):
        user_text_window = tk.Toplevel(self.root)
        user_text_window.title(user)
        user_text_window.geometry("800x600")
        
        text_widget = tk.Text(user_text_window)
        text_widget.pack(expand=True, fill="both")
        
        self.current_user_windows[user] = text_widget
        self.update_text_widget(user, text_widget)
    
    def update_text_widget(self, user, text_widget):
        if user and self.current_scene:
            scene_text = self.users[user].get(self.current_scene, "")
            text_widget.config(state="normal")
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", scene_text)
            text_widget.config(state="disabled")
    
    def view_config(self):
        if self.config_window:
            self.config_window.destroy()

        self.config_window = tk.Toplevel(self.root)
        self.config_window.title("Configuration Actuelle")
        self.config_window.geometry("800x600")
        
        for user, scenes in self.users.items():
            user_label = tk.Label(self.config_window, text=f"Utilisateur: {user}", font=("Arial", 12, "bold"))
            user_label.pack(pady=5)
            
            for scene, text in scenes.items():
                scene_label = tk.Label(self.config_window, text=f"  Scène: {scene} - Texte: {text[:30]}{'...' if len(text) > 30 else ''}")
                scene_label.pack(pady=2)

        tk.Button(self.config_window, text="Supprimer un Utilisateur", command=self.delete_user).pack(pady=10)
        tk.Button(self.config_window, text="Supprimer une Scène", command=self.delete_scene).pack(pady=10)

    def refresh_config_window(self):
        if self.config_window:
            self.view_config()

    def delete_user(self):
        user_name = simpledialog.askstring("Supprimer Utilisateur", "Nom de l'utilisateur à supprimer:")
        if user_name in self.users:
            del self.users[user_name]
            if user_name in self.current_user_windows:
                del self.current_user_windows[user_name]
            messagebox.showinfo("Info", f"Utilisateur {user_name} supprimé avec succès.")
            self.refresh_config_window()
        else:
            messagebox.showerror("Erreur", f"L'utilisateur {user_name} n'existe pas.")
    
    def delete_scene(self):
        scene_name = simpledialog.askstring("Supprimer Scène", "Nom de la scène à supprimer:")
        if scene_name in self.scenes:
            self.scenes.remove(scene_name)
            for user in self.users:
                if scene_name in self.users[user]:
                    del self.users[user][scene_name]
            messagebox.showinfo("Info", f"Scène {scene_name} supprimée avec succès.")
            self.refresh_config_window()
        else:
            messagebox.showerror("Erreur", f"La scène {scene_name} n'existe pas.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PrompteurApp(root)
    root.mainloop()
