import json

with open('./public/Result/mail/531746.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 处理每个stepId的groups
result = []
for step in data['steps']:
    step_id = step['stepId']
    total_attention = 0
    total_boundary = 0
    group_count = len(step['groups'])
    
    for group in step['groups']:
        total_attention += group['ratings']['attention']
        total_boundary += group['ratings']['boundary']
    
    average_attention = total_attention / group_count if group_count > 0 else 0
    average_boundary = total_boundary / group_count if group_count > 0 else 0
    
    result.append({
        'stepId': step_id,
        'average_attention': average_attention,
        'average_boundary': average_boundary
    })

# 输出结果
for res in result:
    print(f"Step ID: {res['stepId']}, Average Attention: {res['average_attention']:.2f}, Average Boundary: {res['average_boundary']:.2f}")

# ./public/Data2/{n}/