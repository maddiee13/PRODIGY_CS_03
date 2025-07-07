import re

class PasswordStrengthChecker:
    def __init__(self, min_length=10):
        self.min_length = min_length

    def check(self, password: str) -> dict:
        feedback = []
        score = 0

        # Length check
        if len(password) >= self.min_length:
            score += 1
            if len(password) >= 14:
                feedback.append("Good password length (14+ characters)")
            else:
                feedback.append(f"Minimum length met ({self.min_length}+ characters)")
        else:
            feedback.append(f"Password should be at least {self.min_length} characters long (current: {len(password)})")

        # Character diversity checks
        checks = [
            (r'[A-Z]', "uppercase letter", "Add uppercase letters (A-Z)"),
            (r'[a-z]', "lowercase letter", "Add lowercase letters (a-z)"),
            (r'\d', "digit", "Include numbers (0-9)"),
            (r'[^A-Za-z0-9]', "special character", "Add special characters (!@#$%^&*)"),
            (r'.{3,}', "repeating patterns", "Avoid repeated patterns")
        ]

        for pattern, positive_fb, negative_fb in checks[:-1]:
            if re.search(pattern, password):
                score += 1
            else:
                feedback.append(negative_fb)

        # Check for repeating patterns
        if not re.search(r'(.)\1{2,}', password):
            score += 0.5
        else:
            feedback.append("Avoid repeating characters (e.g. 'aaa')")

        # Final scoring
        score = min(int(score), 5)  # Cap at 5
        
        strength_levels = {
            5: "Very Strong",
            4: "Strong",
            3: "Medium",
            2: "Weak",
            1: "Very Weak",
            0: "Insecure"
        }
        strength = strength_levels.get(score, "Insecure")

        # Positive feedback for strong passwords
        if score >= 4:
            feedback.insert(0, "Good job! Your password is secure")
        elif score == 0:
            feedback.insert(0, "Immediately change this password - it's extremely vulnerable")

        return {
            "score": score,
            "strength": strength,
            "feedback": feedback
        }