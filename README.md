NAO PLANNING CHALLENGE 2026
===========================
Participants:
- Khushbakht Khan (email: khushbakht.khan3@studio.unibo.it)
- Alishba Khan    (email: alishba.khan2@studio.unibo.it)

------------------------------------
Project Description
------------------------------------
This project brings together a NAO dance behavior made in Choregraphe and a
Python implementation of Algorithm A. The planner is designed to meet these
competition rules:

• An ordered list of mandatory poses from the initial pose to the goal
• Compatible transitions chosen from a supplied movement catalog
• A global minimum of 5 intermediate positions, including mandatory positions
• A total duration no greater than 2 minutes

In `algorithm.py`, movements are connected only when the catalog explicitly
declares compatible start and end poses. Every catalog entry also records its
duration. Algorithm A finds the quickest route through the mandatory poses
while respecting the position minimum and time cap; if no valid route is
available, it reports that rather than producing an invalid sequence.

The behavior currently runs this sequence: `StandInit → Air Guitar → Happy
Birthday → Hello → Wipe Forehead → Tai Chi → Bow → End Pose → Crouch`. It
includes six dance or gesture actions. Their animation timelines take about
72 seconds in total; this estimate does not include the time needed to move
into the opening and closing postures. The soundtrack is triggered alongside
the first dance action.

The exact mandatory poses between `StandInit` and `Crouch`, along with the
competition's transition-compatibility and duration data, are not included
here. As a result, the choreography follows the known start, finish, minimum
position count, and timing guidelines, but still needs to be checked against
the full mandatory-pose list. Provide the assignment data to
`generate_sequence(mandatory_positions, movements)` before considering the
planner's output fully competition-ready.

------------------------------------
How to Run (Simulation)
------------------------------------
1. Launch Choregraphe in the VM.
2. Choose **File → Open Project**.
3. Select `naoproject.pml` in the project root.
4. Connect to the virtual NAO if it is not connected already.
5. Press **Play** to run the behavior.

------------------------------------
Required Libraries / Environment
------------------------------------
• Choregraphe Suite and NAOqi, available in the official VM
• Python 2.7, the VM's default Python version
• No extra Python packages are needed

------------------------------------
Repository Link
------------------------------------
The project repository is available here:
https://github.com/Khushbakhtkhan/NAO-Planning-Challenge-AI-2026

Video Link
---------------
https://drive.google.com/file/d/1veAslMthWHpUO169b8YeTU8Jn-oVLFZ-/view?usp=drive_link
