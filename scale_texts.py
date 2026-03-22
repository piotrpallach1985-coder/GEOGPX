import re

file_path = r"c:\Users\piotr\Desktop\Programy Finalne\GEOGPX Draw & Measure v1.1\GEOGPX Flex v.1.1.html"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Reverse the static matches from the previous 30% reduction.
text = text.replace("text-[8.4px]", "text-xs")
text = text.replace("text-[9.8px]", "text-sm")
text = text.replace("text-[11.2px]", "text-base")
text = text.replace("text-[12.6px]", "text-lg")
text = text.replace("text-[16.8px]", "text-2xl")
text = text.replace("text-[21px]", "text-3xl")
text = text.replace("text-[25.2px]", "text-4xl")
text = text.replace("font = '14px Arial'", "font = '20px Arial'")
text = text.replace("bold ${9.8 / transform.scale}px Arial", "bold ${14 / transform.scale}px Arial")

# Fix the text-xl that collided into text-sm
text = text.replace("md:text-sm flex items-center gap-2", "md:text-xl flex items-center gap-2")
text = text.replace('class="text-sm font-black text-slate-800 mb-2"', 'class="text-xl font-black text-slate-800 mb-2"')

# Reverse arbitrary sizes.
text = text.replace("text-[7px]", "text-[10px]")
text = text.replace("text-[7.7px]", "text-[11px]")
text = text.replace("text-[9.1px]", "text-[13px]")
text = text.replace("text-[10.5px]", "text-[15px]")

# Add body explicit size so that we can inherit the global 10% reduction.
text = text.replace('class="bg-slate-50 text-slate-800 p-4 md:p-8 relative"', 'class="bg-slate-50 text-[14.4px] text-slate-800 p-4 md:p-8 relative"')

# 2. Scale arbitrary text-[xxpx] sizes by 10%. (They were intact).
def scale_10_arb(match):
    val = float(match.group(1))
    new_val = round(val * 0.9, 1)
    if new_val.is_integer(): new_val = int(new_val)
    return f"text-[@@{new_val}px@@]" # Add temporary marker to prevent double scaling

text = re.sub(r"text-\[([0-9.]+)px\]", scale_10_arb, text)

# Scale normal tailwind utilities to 10% reduction and add them as custom pixels
scale_map_10 = {
    r"\btext-xs\b": "text-[10.8px]",
    r"\btext-sm\b": "text-[12.6px]",
    r"\btext-base\b": "text-[14.4px]",
    r"\btext-lg\b": "text-[16.2px]",
    r"\btext-xl\b": "text-[18px]",
    r"\btext-2xl\b": "text-[21.6px]",
    r"\btext-3xl\b": "text-[27px]",
    r"\btext-4xl\b": "text-[32.4px]"
}

for pattern, replacement in scale_map_10.items():
    text = re.sub(pattern, replacement, text)

# Remove temporary markers
text = text.replace("text-[@@", "text-[")
text = text.replace("px@@]", "px]")

# Canvas text scaling
text = text.replace("font = '20px Arial'", "font = '18px Arial'")
text = text.replace("bold ${14 / transform.scale}px Arial", "bold ${12.6 / transform.scale}px Arial")

# 3. Apply custom -20% and -30% overrides
# GEOGPX Flex title: 20% smaller than ORIGINAL.
# Original: text-2xl md:text-3xl (24px, 30px) -> -20%: 19.2px, 24px.
# After 10% reduction above, it became text-[21.6px] md:text-[27px]
text = text.replace('class="text-[21.6px] md:text-[27px] font-extrabold mb-2 text-blue-600">GEOGPX Flex',
                    'class="text-[19.2px] md:text-[24px] font-extrabold mb-2 text-blue-600">GEOGPX Flex')

# Load / Save buttons: 30% smaller than ORIGINAL.
# Original emojis: text-lg (18px) -> -30%: 12.6px.
# Original labels had NO text scale class, so inherited body (16px) -> -30% = 11.2px
# After 10% reduction, emojis are: text-[16.2px].
# So we target the buttons exactly.
target_btn1 = '''<label for="projectInputTop" class="cursor-pointer bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2.5 px-6 rounded-lg transition shadow-sm flex items-center justify-center gap-2">
                    <span class="text-[16.2px]">📂</span> <span data-i18n="btnLoadProject">Wczytaj projekt</span>'''
replacement_btn1 = '''<label for="projectInputTop" class="cursor-pointer bg-indigo-500 hover:bg-indigo-600 text-[11.2px] text-white font-bold py-2.5 px-6 rounded-lg transition shadow-sm flex items-center justify-center gap-2">
                    <span class="text-[12.6px]">📂</span> <span data-i18n="btnLoadProject">Wczytaj projekt</span>'''
text = text.replace(target_btn1, replacement_btn1)

target_btn2 = '''<button id="btnExportTop" class="bg-amber-500 hover:bg-amber-600 text-white font-bold py-2.5 px-6 rounded-lg transition shadow-sm flex items-center justify-center gap-2">
                    <span class="text-[16.2px]">💾</span> <span data-i18n="btnSave">Zapisz projekt</span>'''
replacement_btn2 = '''<button id="btnExportTop" class="bg-amber-500 hover:bg-amber-600 text-[11.2px] text-white font-bold py-2.5 px-6 rounded-lg transition shadow-sm flex items-center justify-center gap-2">
                    <span class="text-[12.6px]">💾</span> <span data-i18n="btnSave">Zapisz projekt</span>'''
text = text.replace(target_btn2, replacement_btn2)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Text adjusted successfully to new requirements.")
