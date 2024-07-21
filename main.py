import tkinter as tk
from tkinter import messagebox

class CardCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Counter for Shotgun Roulette")
        
        # Initialize variables
        self.num_live = 0
        self.num_blank = 0
        self.total_rounds = 0
        self.rounds_info = []
        self.selected_circle = None

        # Create UI elements
        self.create_widgets()
    
    def create_widgets(self):
        # Buttons and labels
        self.mark_blank_button = tk.Button(self.root, text="Mark as Blank", command=self.mark_blank)
        self.mark_blank_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.mark_live_button = tk.Button(self.root, text="Mark as Live", command=self.mark_live)
        self.mark_live_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.mark_unknown_button = tk.Button(self.root, text="Mark as Unknown", command=self.mark_unknown)
        self.mark_unknown_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_game)
        self.reset_button.grid(row=0, column=3, padx=10, pady=10)
        
        self.instructions_label = tk.Label(self.root, text="Enter number of live and blank rounds:")
        self.instructions_label.grid(row=1, column=0, columnspan=4, pady=(10, 0))
        
        self.blank_label = tk.Label(self.root, text="Number of Blank Rounds:")
        self.blank_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        
        self.blank_entry = tk.Entry(self.root)
        self.blank_entry.grid(row=2, column=1, padx=10, pady=5)
        
        self.live_label = tk.Label(self.root, text="Number of Live Rounds:")
        self.live_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        
        self.live_entry = tk.Entry(self.root)
        self.live_entry.grid(row=3, column=1, padx=10, pady=5)
        
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_rounds)
        self.submit_button.grid(row=4, column=0, columnspan=4, pady=10)
        
        # Placeholder for circles
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg='gray')
        self.canvas.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        # Bind canvas click event
        self.canvas.bind("<Button-1>", self.select_circle)

        self.create_circles()
    
    def create_circles(self):
        self.canvas.delete("all")
        self.rounds_info = []
        self.text_items = []
        self.ratios = []
        for i in range(self.total_rounds):
            x = 50 + i * 70
            y = 100
            circle = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill='purple', outline='black', width=1)
            text_item = self.canvas.create_text(x, y + 25, text="0.0%", fill='black')
            ratio_item = self.canvas.create_text(x, y + 40, text=f"{self.num_live}:{self.num_blank}", fill='black')
            self.rounds_info.append({
                'id': circle,
                'status': 'unknown',
                'text_item': text_item,
                'ratio_item': ratio_item
            })
    
    def mark_blank(self):
        if self.selected_circle is not None:
            self.update_circle_color(self.selected_circle, 'blue')
    
    def mark_live(self):
        if self.selected_circle is not None:
            self.update_circle_color(self.selected_circle, 'red')

    def mark_unknown(self):
        if self.selected_circle is not None:
            self.update_circle_color(self.selected_circle, 'purple')

    def update_circle_color(self, circle_id, color):
        for round_info in self.rounds_info:
            if round_info['id'] == circle_id:
                if color == 'red':
                    if round_info['status'] == 'blank':
                        messagebox.showerror("Error", "Cannot mark as live, already marked as blank.")
                        return
                    round_info['status'] = 'live'
                elif color == 'blue':
                    if round_info['status'] == 'live':
                        # Allow marking blue to live without error
                        round_info['status'] = 'live'
                    else:
                        round_info['status'] = 'blank'
                elif color == 'purple':
                    round_info['status'] = 'unknown'
                
                # Update circle appearance and reset selection
                self.canvas.itemconfig(circle_id, fill=color)
                if self.selected_circle is not None:
                    self.canvas.itemconfig(self.selected_circle, outline='black', width=1)
                self.selected_circle = None
                self.update_likelihoods()
                break
    
    def update_likelihoods(self):
        live_count = sum(1 for round_info in self.rounds_info if round_info['status'] == 'live')
        blank_count = sum(1 for round_info in self.rounds_info if round_info['status'] == 'blank')
        remaining_rounds = self.total_rounds - live_count - blank_count

        if remaining_rounds > 0:
            for round_info in self.rounds_info:
                if round_info['status'] == 'unknown':
                    likelihood = (self.num_live - live_count) / remaining_rounds * 100
                    likelihood = max(min(likelihood, 100), 0)  # Cap at 100% and ensure non-negative
                    self.canvas.itemconfig(round_info['text_item'], text=f"{likelihood:.1f}%")
                    self.canvas.itemconfig(round_info['ratio_item'], text=f"{self.num_live - live_count}:{self.num_blank - blank_count}")
                elif round_info['status'] == 'live':
                    self.canvas.itemconfig(round_info['text_item'], text="100.0%")
                    self.canvas.itemconfig(round_info['ratio_item'], text="")
                elif round_info['status'] == 'blank':
                    self.canvas.itemconfig(round_info['text_item'], text="0.0%")
                    self.canvas.itemconfig(round_info['ratio_item'], text="")
        else:
            # If no remaining unknown rounds, set all to 0% or 100% based on status
            for round_info in self.rounds_info:
                if round_info['status'] == 'live':
                    self.canvas.itemconfig(round_info['text_item'], text="100.0%")
                    self.canvas.itemconfig(round_info['ratio_item'], text="")
                elif round_info['status'] == 'blank':
                    self.canvas.itemconfig(round_info['text_item'], text="0.0%")
                    self.canvas.itemconfig(round_info['ratio_item'], text="")
                elif round_info['status'] == 'unknown':
                    self.canvas.itemconfig(round_info['ratio_item'], text=f"{self.num_live - live_count}:{self.num_blank - blank_count}")
    
    def select_circle(self, event):
        circle_id = self.canvas.find_closest(event.x, event.y)[0]
        if circle_id in [round_info['id'] for round_info in self.rounds_info]:
            if self.selected_circle is not None:
                if self.selected_circle != circle_id:
                    self.canvas.itemconfig(self.selected_circle, outline='black', width=1)
            self.selected_circle = circle_id
            self.canvas.itemconfig(self.selected_circle, outline='pink', width=3)
        else:
            if self.selected_circle is not None:
                self.canvas.itemconfig(self.selected_circle, outline='black', width=1)
                self.selected_circle = None

    def submit_rounds(self):
        try:
            self.num_blank = int(self.blank_entry.get())
            self.num_live = int(self.live_entry.get())
            self.total_rounds = self.num_blank + self.num_live
            if self.total_rounds > 8:
                messagebox.showwarning("Warning", "Gun Ammo Max Count Exceeded")
                return
            self.create_circles()
            self.update_likelihoods()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
    
    def reset_game(self):
        self.num_live = 0
        self.num_blank = 0
        self.total_rounds = 0
        self.rounds_info = []
        self.selected_circle = None
        self.canvas.delete("all")
        self.create_circles()
        self.update_likelihoods()
        self.canvas.bind("<Button-1>", self.select_circle)  # Rebind circle selection

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = CardCounterApp(root)
    app.start()
