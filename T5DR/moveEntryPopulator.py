import tkinter as tk
import re

def generate_output():
    user_id = id_entry.get().strip()
    if not user_id:
        user_id = "Unknown"  # fallback just in case

    user_input = entry.get("1.0", tk.END).strip()
    lines = user_input.splitlines()
    output = []

    for line in lines:
        parts = line.split('\t')
        if len(parts) != 7:
            continue

        input_value = parts[0]
        target = parts[1]
        damage = parts[2]
        startup = parts[3]
        block = parts[4]
        hit = parts[5]
        ch = parts[6]

        hit_match = re.match(r'([-+±]?\??\d*)(.*)', hit)
        ch_match = re.match(r'([-+±]?\??\d*)(.*)', ch)

        hit_num = hit_match.group(1) if hit_match else hit
        hit_annotation = hit_match.group(2) if hit_match else ''

        ch_num = ch_match.group(1) if ch_match else ch
        ch_annotation = ch_match.group(2) if ch_match else ''

        ch_field = f"|ch={ch_num}{ch_annotation}\n" if (hit_num != ch_num or hit_annotation != ch_annotation) else "|ch=\n"

        move_template = (
            "{{Move\n"
            f"|id={user_id}-{input_value}\n"
            f"|num=\n"
            "|parent=\n"
            f"|input={input_value}\n"
            "|alias=\n"
            "|alt=\n"
            "|name=\n"
            f"|target={target}\n"
            f"|damage={damage}\n"
            f"|startup=i{startup}\n"
            f"|block={block}\n"
            f"|hit={hit_num}{hit_annotation}\n"
            f"{ch_field}"
            "|crush=\n"
            "|recv=\n"
            "|tot=\n"
            "|range=\n"
            "|tracksLeft=\n"
            "|tracksRight=\n"
            "|image=\n"
            "|video=\n"
            "|notes=\n"
            "}}"
        )

        output.append(move_template)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "\n".join(output))

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(output_text.get("1.0", tk.END))
    root.update()

# GUI setup
root = tk.Tk()
root.title("Move Data Formatter")
root.geometry("800x800")

# Character ID input
id_label = tk.Label(root, text="Enter character ID:")
id_label.pack()
id_entry = tk.Entry(root, width=50)
id_entry.insert(0, "Yoshimitsu")  # default value
id_entry.pack()

label = tk.Label(root, text="Enter move data from SDTEKKEN (7 parts):")
label.pack()

entry = tk.Text(root, height=10, width=50)
entry.pack()

button = tk.Button(root, text="Generate", command=generate_output)
button.pack()

output_text = tk.Text(root, height=30, width=50)
output_text.pack()

copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack()

root.mainloop()
