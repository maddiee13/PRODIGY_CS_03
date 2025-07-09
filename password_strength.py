import re
import math

class PasswordStrengthChecker:
    def __init__(self, min_length=10):
        self.min_length = min_length

    def estimate_crack_time(self, password: str) -> str:
        # Estimate entropy
        charset = 0
        if re.search(r'[a-z]', password):
            charset += 26
        if re.search(r'[A-Z]', password):
            charset += 26
        if re.search(r'\d', password):
            charset += 10
        if re.search(r'[^A-Za-z0-9]', password):
            charset += 32  # Approximate for special chars
        if charset == 0:
            charset = 1
        entropy = len(password) * math.log2(charset)
        # Estimate guesses per second (offline fast attack)
        guesses_per_second = 1e10
        guesses = 2 ** entropy
        seconds = guesses / guesses_per_second
        # Convert seconds to human readable
        def human_time(seconds):
            intervals = [
                ('years', 60*60*24*365),
                ('days', 60*60*24),
                ('hours', 60*60),
                ('minutes', 60),
                ('seconds', 1)
            ]
            result = []
            for name, count in intervals:
                value = int(seconds // count)
                if value:
                    seconds -= value * count
                    result.append(f"{value} {name}")
            if not result:
                return "less than a second"
            return ', '.join(result[:2])
        return human_time(seconds)

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
        # Crack time estimate
        crack_time = self.estimate_crack_time(password)
        return {
            "score": score,
            "strength": strength,
            "feedback": feedback,
            "crack_time": crack_time
        }