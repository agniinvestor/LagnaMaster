Detect rework in this session and enforce lessons-learned entry if found.

Run the following steps in sequence:

## Step 1: Run rework detection

Run `.venv/bin/python tools/rework_counter.py --commits 20` from the repo root. Capture the full output.

If the user provided $ARGUMENTS, use it as the --since ref instead:
`.venv/bin/python tools/rework_counter.py --since $ARGUMENTS`

## Step 2: Evaluate results

Check the exit code:
- **Exit 0 (no rework):** Print "No rework detected in recent commits." and stop.
- **Exit 1 (rework detected):** Continue to Step 3.
- **Exit 2 (error):** Print the error and stop.

## Step 3: Analyze the rework pattern

From the rework report output, identify:
1. Which commits were flagged and why (keyword match or file iteration)
2. What the root cause pattern is (one of: missing control, scope creep, anchoring, mixed session types, untested locally, protocol skipped, etc.)
3. Which files were affected

## Step 4: MANDATORY — Draft a lessons_learned entry

This is NOT optional. Every rework detection MUST produce a lesson.

Draft an entry using this exact format:

```
## L0NN: [Descriptive Title] (S[current session])

**What:** [Specific failure — what happened, what triggered the rework commits?]
**Cost:** [Number of rework commits, files affected, time wasted]
**Control:** [What code enforcement, hook, or gate would prevent this from recurring?]
**Would catch?** [Yes/No + explain the mechanism]
```

Requirements for the entry:
- The **What** must be specific to THIS session, not generic
- The **Cost** must include concrete numbers from the rework report
- The **Control** must be a CODE enforcement (not a memory protocol — L008 proves those fail)
- The **Would catch** must explain the detection mechanism

## Step 5: Present for confirmation

Show the drafted entry and ask: "Add this to lessons_learned.md? (I will assign the next L-number automatically.)"

Once confirmed:
1. Read the current lessons_learned.md (check both `/Users/harsh/.claude/projects/-Users-harsh/memory/lessons_learned.md` and any project-local copy)
2. Determine the next L-number by finding the highest existing one
3. Append the entry before the TEMPLATE section
4. Update the OPEN LOOPS table if the control is not yet built (status: OPEN)
5. Update the document header count

## Step 6: Recommend control implementation

After adding the lesson, print:

```
NEXT STEP: Build the control described in L0NN.
A lesson without a control is an open loop. Close it before the session ends.
```

Do not ask for confirmation on intermediate steps. Run the detection, analyze, draft, and present in one flow.
