"""
CISC-121 Project: Bubble Sort Interactive Visualizer
Author: Trevin Singaraja
Description: A step-by-step educational app that demonstrates Bubble Sort
             using an interactive Gradio interface.
"""
 
import gradio as gr
 
 
# ─────────────────────────────────────────────
# ALGORITHM: Bubble Sort
# ─────────────────────────────────────────────
 
def bubble_sort_steps(arr):
    """
    Perform Bubble Sort and record every comparison/swap as a step.
 
    How Bubble Sort works:
    - Compare adjacent elements; if the left is larger, swap them.
    - Repeat passes until no swaps occur (list is sorted).
    - Each full pass bubbles the largest unsorted value to the end.
    """
    arr = arr[:]
    steps = []
    n = len(arr)
 
    for pass_num in range(n - 1):  # We need at most n-1 passes
        swapped = False
 
        for i in range(n - 1 - pass_num):
            comparing = (i, i + 1)
 
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
                steps.append({
                    "array": arr[:],
                    "comparing": comparing,
                    "swapped": True,
                    "pass": pass_num + 1,
                    "sorted_boundary": n - pass_num - 1,
                })
            else:
                steps.append({ # Record the comparison even if no swap occurs
                    "array": arr[:],
                    "comparing": comparing,
                    "swapped": False,
                    "pass": pass_num + 1,
                    "sorted_boundary": n - pass_num - 1,
                })
 
        if not swapped:
            break
 
    return arr, steps
 
 
# ─────────────────────────────────────────────
# RENDERING
# ─────────────────────────────────────────────
 
def render_array(array, comparing, sorted_boundary): # Visualize the array with indicators for comparisons and sorted portion
    result = []
    for idx, val in enumerate(array):
        if idx in comparing:
            result.append(f"[{val}]")
        elif idx >= sorted_boundary:
            result.append(f"✓{val}")
        else:
            result.append(str(val))
    return "  ".join(result)
 
 
def format_all_steps(steps, original, final): # Create a detailed trace of all steps with visual indicators
    if not steps:
        return "✅ Array was already sorted — no steps needed!"
 
    lines = [f"📋 Original array:  {original}\n"]
    current_pass = 0
 
    for step_num, step in enumerate(steps, start=1):
        if step["pass"] != current_pass:
            current_pass = step["pass"]
            lines.append(f"\n── Pass {current_pass} ──────────────────────────")
 
        i, j = step["comparing"]
        action = "🔄 SWAP" if step["swapped"] else "  OK  "
        visual = render_array(step["array"], step["comparing"], step["sorted_boundary"])
        lines.append(
            f"Step {step_num:>3}  |  Compare positions {i} & {j}  →  {action}\n"
            f"         {visual}"
        )
 
    lines.append(f"\n✅ Sorted array:    {final}")
    lines.append(f"\nTotal comparisons: {len(steps)}")
    lines.append(f"Total swaps:       {sum(1 for s in steps if s['swapped'])}")
    return "\n".join(lines)
 
 
# ─────────────────────────────────────────────
# INPUT VALIDATION
# ─────────────────────────────────────────────
 
def parse_input(raw_input):
    raw_input = raw_input.strip().strip("[]")
 
    if not raw_input:
        return None, "⚠️ Please enter at least two numbers."
 
    parts = raw_input.split(",") # Split by commas to allow flexible input formats
    numbers = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        try:
            numbers.append(int(part))
        except ValueError:
            return None, f"⚠️ '{part}' is not a valid integer. Use whole numbers only."
 
    if len(numbers) < 2:
        return None, "⚠️ Please enter at least two numbers to sort."
 
    if len(numbers) > 20:
        return None, "⚠️ Please enter 20 numbers or fewer."
 
    return numbers, None
 
 
# ─────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────
 
def run_bubble_sort(raw_input):
    numbers, error = parse_input(raw_input)
 
    if error:
        return error, "", ""
 
    original = numbers[:]
    sorted_arr, steps = bubble_sort_steps(numbers)
    trace = format_all_steps(steps, original, sorted_arr)
 
    summary = (
        f"Input:   {original}\n"
        f"Output:  {sorted_arr}\n"
        f"Steps:   {len(steps)} comparisons, "
        f"{sum(1 for s in steps if s['swapped'])} swaps"
    )
 
    explanation = (       # Provide a concise explanation of how Bubble Sort works and its complexities
        "How Bubble Sort works:\n"
        "1. Compare each pair of adjacent elements.\n"
        "2. If the left element is larger, swap them.\n"
        "3. Repeat for every pair in the unsorted portion.\n"
        "4. Each full pass moves the largest remaining value to the end.\n"
        "5. Stop when a full pass completes with no swaps.\n\n"
        "Time Complexity:\n"   
        "  Best case:    O(n)   — already sorted\n"
        "  Average case: O(n²)\n"
        "  Worst case:   O(n²)  — reverse sorted\n\n"
        "Space Complexity: O(1)  — sorts in place"
    )
 
    return summary, trace, explanation
 
 
# ─────────────────────────────────────────────
# GRADIO UI
# ─────────────────────────────────────────────
 
with gr.Blocks(title="Bubble Sort Visualizer") as demo:
 
    gr.Markdown("# 🫧 Bubble Sort Interactive Visualizer")
    gr.Markdown(
        "Enter a list of integers to see **every comparison and swap** "
        "that Bubble Sort performs, step by step."
    )
 
    with gr.Row():
        with gr.Column(scale=2):
            input_box = gr.Textbox(
                label="Enter numbers (comma-separated)",
                placeholder="e.g.  5, 3, 8, 1, 9, 2",
                lines=1,
            )
            sort_btn = gr.Button("▶ Run Bubble Sort", variant="primary")
 
        with gr.Column(scale=1):
            gr.Markdown("### Try these examples")
            gr.Examples(
                examples=[
                    ["5, 3, 8, 1, 9, 2"],
                    ["10, 7, 4, 2, 1"],
                    ["1, 2, 3, 4, 5"],
                    ["5, 4, 3, 2, 1"],
                    ["42, 7, 99, 3, 55, 21, 8"],
                ],
                inputs=input_box,
            )
 
    summary_box = gr.Textbox(label="📊 Result Summary", lines=4, interactive=False)
    trace_box = gr.Textbox(
        label="🔍 Step-by-Step Trace  ( [x] = being compared | ✓x = already sorted )",
        lines=20,
        interactive=False, 
    )
    explanation_box = gr.Textbox(
        label="📚 Algorithm Explanation & Complexity",
        lines=12,
        interactive=False,
    )
 
    sort_btn.click(
        fn=run_bubble_sort,
        inputs=input_box,
        outputs=[summary_box, trace_box, explanation_box],
    )
 
    gr.Markdown("---\n*CISC-121 Project · Bubble Sort Visualizer · Built with Gradio*")
 
if __name__ == "__main__":
    demo.launch()