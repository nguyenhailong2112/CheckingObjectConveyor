# Retraining Trigger & A/B Gate Template

## Trigger conditions
- Accuracy drop > 2%
- Uncertain rate increase > 5%
- New object category/packaging appears
- Significant overlap failure increase

## A/B validation
- Model A (current)
- Model B (candidate)

Required metrics:
- Count accuracy
- Double count rate
- Miss count rate
- Uncertain rate
- FPS

Decision:
- Deploy B only if B >= A on acceptance KPI gate.