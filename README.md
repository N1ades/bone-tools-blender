# BoneTools for Blender

## Description  
**BoneTools for Blender** is a lightweight Blender add-on designed to streamline vertex weight editing and bone management for rigging workflows. It provides operators to automate tasks such as copying vertex weights between bones and fixing vertex groups with inconsistent naming conventions. The tools integrate seamlessly into Blender's 3D Viewport UI.

---

## Features  
- **Copy Weights:**  
  Automatically transfers vertex weights from multiple selected bones to an active bone. After transferring, it optionally removes the source bones for a cleaner rig.

- **Fix Groups:**  
  Corrects weight groups by converting names with underscores (`_`) to dot notation (`.`) if the corresponding dot notation group exists.

- **Custom Panel UI:**  
  Accessible under the **Tool** tab in the Weight Paint mode for intuitive usage.

---

## Installation  
1. Download the `bonetools.py` file.
2. Open Blender and navigate to `Edit > Preferences > Add-ons`.
3. Click `Install...`, select the `bonetools.py` file, and enable the add-on.
4. Access the tools under the **Tool** tab in the 3D Viewport's sidebar.

---

## Usage  
1. **Copy Weights:**
   - Select bones in Pose Mode.
   - Set the active bone as the target bone.
   - Use the **Copy Weights** button in the custom panel.
   - Automatically merge weights and clean up unnecessary bones.

2. **Fix Groups:**
   - Select affected bones in Pose Mode.
   - Use the **Fix Groups** button in the custom panel to resolve naming mismatches.

---

## Dependencies  
- Blender 2.80+  
- Python 3.7+  

---

## License  
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## Contributing  
Contributions are welcome! Submit issues or pull requests to improve functionality or add new features.  

---

## Contact  
For questions, feedback, or support, feel free to reach out via the project's GitHub repository.
