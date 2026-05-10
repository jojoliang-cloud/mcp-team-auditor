from datetime import datetime, timezone

class RepoScorer:
    def analyze(self, repo_data):
        score = 0.0
        risks = []
        
        last_update = repo_data.get("last_updated")
        if last_update:
            # Ensure last_update is timezone-aware
            if last_update.tzinfo is None:
                last_update = last_update.replace(tzinfo=timezone.utc)
            days = (datetime.now(timezone.utc) - last_update).days
            if days > 365:
                risks.append(f"维护风险：停更 {days} 天")
                score += 0.5
        
        if not repo_data.get("has_license"):
            risks.append("法律风险：无开源协议")
            score += 0.4
            
        issues = repo_data.get("open_issues", 0)
        stars = repo_data.get("stars", 1)
        if issues / (stars + 1) > 0.15:
            risks.append("社区风险：Issue堆积过高")
            score += 0.2

        level = "LOW"
        if score >= 0.7: level = "HIGH"
        elif score >= 0.3: level = "MEDIUM"
        
        return {
            "score": round(score, 2),
            "risk_level": level,
            "reason_list": risks
        }
