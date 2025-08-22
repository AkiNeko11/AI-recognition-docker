from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import os
from ultralytics import YOLO

app = Flask(__name__)
CORS(app) 

# 创建必要目录
os.makedirs('uploads', exist_ok=True)

# 加载YOLO模型
try:
    model = YOLO('best.pt')  # 模型文件名为best.pt
    print("YOLO模型加载成功")
except Exception as e:
    print(f"模型加载失败: {e}")
    model = None

# 数据库
obj_DB = {
    'CT': {'introduction': 'CT'},
    'T': {'introduction': 'T'},
}

def get_obj_info(obj_name):
    return obj_DB.get(obj_name, {
        'introduction': f'这是{obj_name}的信息'
    })

@app.route('/health', methods=['GET'])
def health_check():
    model_status = "loaded" if model is not None else "failed"
    return jsonify({
        'status': 'healthy', 
        'service': 'AI Recognition Service',
        'model_status': model_status
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({'error': '模型未加载'}), 500
            
        if 'image' not in request.files:
            return jsonify({'error': '没有图片文件'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': '文件名不能为空'}), 400
        
        # 处理图片
        image = Image.open(file.stream)
        
        # YOLO模型预测
        results = model(image,conf=0.5,iou=0.5)         # 置信度0.5，重叠去除0.5
        
        # 解析YOLO结果
        objs = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # 获取类别ID和置信度
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    
                    # 获取类别名称
                    class_name = model.names[class_id]
                    
                    # 只保留置信度高于0.5的结果
                    if confidence > 0.5:
                        obj_info = get_obj_info(class_name)
                        
                        objs.append({
                            'name': class_name,
                            'confidence': round(confidence, 3),
                            'Info': obj_info
                        })
        
        if not objs:
            return jsonify({'error': '图片中未识别到物体'}), 400
            
        return jsonify({'objs': objs})
        
    except Exception as e:
        return jsonify({'error': f'识别失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 