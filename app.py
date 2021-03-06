from flask import Flask, request, jsonify, Response
app = Flask(__name__)

tmpRecipe = {
    "id":"12345", 
    "name":"백종원의 부대찌개", 
    "chef":"백종원",
    "menu":"부대찌개",
    "ingredients":["햄", "라면사리", "고추가루", "파"],
    "steps": [
        "냄비에 물을 500ml 끓이세요",
        "수프를 넣으세요",
        "면을 넣으세요",
        "3분간 더 끓이면 완성"
        ]
}

@app.route("/")
def helloWorld():
    return "HelloWorld";

#심사를 위한 health
@app.route("/health", methods=["GET"])
def health():
    return Response("OK", status=200);

#레시피 랜덤추천
@app.route("/recommendRecipe", methods=["POST"])
def recommendRecipe():
    return jsonify(tmpRecipe["name"]);

#메뉴명으로 레시피 랜덤추천
@app.route("/recommendRecipeByMenu", methods=["POST"])
def recommendRecipeByMenu():
    req = request.json
    menu = req['action']['parameters']['menu']['value']
    result = {
        "id": tmpRecipe["id"],
        "name": tmpRecipe["name"]
        }
    return jsonify(result);

#셰프명으로 레시피 랜덤추천
@app.route("/recommendRecipeByChef", methods=["POST"])
def recommendRecipeByChef():
    req = request.json
    chef = req['action']['parameters']['chef']['value']
    result = {
        "id": tmpRecipe["id"],
        "name": tmpRecipe["name"]
        }
    return jsonify(result);

#레시피에서스텝찾기
@app.route("/answerStepFromRecipeByStepNo", methods=["POST"])
def answerStepFromRecipeByStepNo():
    req = request.json
    # step = req['action']['parameters']['step']['value']
    step = 3;
    result = {
        "id": tmpRecipe["id"],
        "step": tmpRecipe["steps"][step],
        "stepNo": step
        }
    return jsonify(result);

#레시피에서재료찾기
@app.route("/answerFromIngredientsFromRecipe", methods=["POST"])
def answerFromIngredientsFromRecipe():
    req = request.json
    # recipe = req['action']['parameters']['recipe']['value']
    result = {
        "id": tmpRecipe["id"],
        "ingredients": tmpRecipe["ingredients"]
        }
    return jsonify(result);

if __name__ == '__main__':
    app.run(host='your.domain.com',port=5000)# your.domain.com 을 사용중인 도메인 명으로 바꿔주세요
