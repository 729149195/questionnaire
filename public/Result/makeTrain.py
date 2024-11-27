import json

with open('./public/Result/mail/531746.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 处理每个stepId的groups
result = []
for step in data['steps']:
    step_id = step['stepId']
    total_attention = 0
    total_correlation_strength = 0
    total_exclusionary_force = 0
    group_count = len(step['groups'])
    
    for group in step['groups']:
        total_attention += group['ratings']['attention']
        total_correlation_strength+= group['ratings']['correlation_strength']
        total_exclusionary_force += group['ratings']['exclusionary_force']
    
    average_attention = total_attention / group_count if group_count > 0 else 0
    average_correlation_strength = total_correlation_strength / group_count if group_count > 0 else 0
    average_exclusionary_force = total_exclusionary_force / group_count if group_count > 0 else 0
    
    result.append({
        'stepId': step_id,
        'average_attention': average_attention,
        'average_correlation_strength': average_correlation_strength,
        'average_exclusionary_force': average_exclusionary_force
    })

# 输出结果
for res in result:
    print(f"Step ID: {res['stepId']}, Average Attention: {res['average_attention']:.2f}, Average correlation_strength: {res['average_correlation_strength']:.2f}, Average exclusionary_force: {res['average_exclusionary_force']:.2f}")

# ./public/Data2/{n}/