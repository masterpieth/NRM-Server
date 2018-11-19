from flask import Flask, request, jsonify, Response
from service.recipeService import *
from dao.recipeDao import *

app = Flask(__name__)
session ={}

def checkMenuExist():
    if 'menuName' in session:
        menuExist = "true"
    else:
        menuExist = "false"
    return menuExist

#0. 심사를 위한 health
@app.route("/health", methods=["GET"])
def health():
    return Response("OK", status=200)

#1. 메뉴추천
@app.route("/answerMenuRecommendation", methods=["POST"])
def answerMenuRecommendation():
    recipe = recommendRecipe()
    session['menuName'] = recipe['menu']
    res = {
        "version": "1.0",
        "resultCode": "OK",
        "output": {
            "menuNameWhenAnswerMenu":session['menuName']
        }
    }
    print("response")
    print(session['menuName'])
    return jsonify(res)
    
# #2. 레시피 추천
# @app.route("/answerRecipe", methods=["POST"])
# def answerRecipe():
#     req = request.json
#     res = {
#         # "booleanMenuExistWhenAnswerRecipe": checkMenuExist()
#     }
#     return jsonify(res)

@app.route("/answerRecipeWithoutMenu", methods=["POST"])
def answerRecipeWithoutMenu():
    menuExist = checkMenuExist()
    res = {
        "version": "1.0",
        "resultCode": "OK",
        "output": {
            "booleanMenuExistWhenAnswerRecipe": menuExist,
        }
    }
    return jsonify(res)

@app.route("/answerRecipeIfMenuExists", methods=["POST"])
def answerRecipeIfMenuExists():
    print("브랜치타고 들어옴")
    req = request.json
    menuName = session['menuName']
    recipe = getRecipeByMenu(menuName) #이거 만들어야 됨
    session['recipeName'] = recipe['name']
    session['menuName'] = menuName
    session['chefName'] = recipe['chef']
    session['step'] = recipe['steps'][0]
    res = {
        "version": "1.0",
        "resultCode": "OK",
        "output": {
            "booleanMenuExistWhenAnswerRecipe": checkMenuExist(),
            "recipeNameWhenAnswerRecipe": session['recipeName'],
            "stepWhenAnswerRecipe": session['step']
        }
    }
    return jsonify(res)

@app.route("/answerRecipeByChef", methods=["POST"])
def answerRecipeByChef():
    res = {
        "version": "1.0",
        "resultCode": "OK",
        "output": {
            "booleanMenuExistWhenAnswerRecipe": checkMenuExist(),
        }
    }
    return jsonify(res)

@app.route("/answerRecipeByChefIfServerMenuExist", methods=["POST"])
def answerRecipeByChefIfServerMenuExist():

@app.route("/answerRecipeByChefIfServerMenuNone", methods=["POST"])
def answerRecipeByChefIfServerMenuNone():

@app.route("/answerRecipeByMenu", methods=["POST"])
def answerRecipeByMenu():
    req = request.json
    menuName = req['action']['parameters']['menuNameWhenAnswerRecipe']['value']
    recipe = getRecipeByMenu(menuName) #이거 만들어야 됨
    session['recipeName'] = recipe['name']
    session['chefName'] = recipe['chef']
    session['menuName'] = menuName
    session['step'] = recipe['steps'][0]
    res = {
        "version": "1.0",
        "resultCode": "OK",
        "output": {
            "recipeNameWhenAnswerRecipe": session['recipeName'],
            "stepWhenAnswerRecipe": session['step']
        }
    }
    return jsonify(res)

@app.route("/answerRecipeByMenuAndChef", methods=["POST"])
def answerRecipeByMenuAndChef():
    print("메뉴이름이랑 셰프이름 받을 때")
    req = request.json
    chefName = req['action']['parameters']['chefNameWhenAnswerRecipe']['value']
    menuName = req['action']['parameters']['menuNameWhenAnswerRecipe']['value']
    recipe = getRecipeByMenuAndChef(menuName, chefName) #이거 만들어야 됨
    session['recipeName'] = recipe['name']
    session['step'] = recipe['steps'][0]
    session['menuName'] = menuName
    session['chefName'] = chefName
    res = {
        "version": "1.0",
        "resultCode": "OK",
        "output": {
            "chefNameWhenAnswerRecipe": session['chefName'],
            "menuNameWhenAnswerRecipe": session['menuName'],
            "recipeNameWhenAnswerRecipe": session['recipeName'],
            "stepWhenAnswerRecipe": session['step']
        }
    }

# #3. 재료묻기
# @app.route("/answerIngredients", methods=["POST"])
# def answerIngredients():
#     req = request.json
#     if 'MENU' not in req['action']['parameters']:
#         if 'menu' not in session:
#             res = {
#                 "version": "1.0",
#                 "resultCode": "BAD"
#             }
#         else:
#             menu = session['menu']
#             recipe = recommendRecipeByMenu(menu) #이거 만들어야 됨
#             session['recipe'] = recipe
#             ingredients = recipe.ingredients
#             res = {
#                 "version": "1.0",
#                 "resultCode": "OK",
#                 "output": {
#                     "menu": menu,
#                     "ingredients": recipe
#                 }
#             }
#     else:
#         menu = req['action']['parameters']['MENU']['value']
#         recipe = recommendRecipeByMenu(menu) #이거 만들어야 됨
#         ingredients = recipe.ingredients
#         res = {
#             "version": "1.0",
#             "resultCode": "OK",
#             "output": {
#                 "menu": menu,
#                 "ingredients": recipe
#             }
#         }
#     return jsonify(res)

# #4. 스텝이동
# @app.route("/answerNextStep", methods=["POST"])
# def answerNextStep():
#     req = request.json
#     if 'recipe' not in session:
#         res = {
#             "version": "1.0",
#             "resultCode": "BAD"
#         }
#     else:
#         recipe = session['recipe']
#         if 'state' not in req['action']['parameters'] and 'stepNo' in req['action']['parameters']:
#             stepNo = req['action']['parameters']['stepNo']['value']
#             session['stepNo'] = stepNo
#             recipeStep = recipe.step[stepNo]
#             res = {
#                 "version": "1.0",
#                 "resultCode": "OK",
#                 "output": {
#                     "recipeStep": recipeStep,
#                     "stepNo": stepNo 
#                 }
#             }
#         elif 'state' in req['action']['parameters'] and 'stepNo' not in req['action']['parameters']:
#                 state = req['action']['parameters']['state']['value']
#                 curStepNo = session['stepNo']+state
#                 recipeStep = recipe.step[curStepNo]
#                 session['stepNo'] = curStepNo
#                 res = {
#                     "version": "1.0",
#                     "resultCode": "OK",
#                     "output": {
#                         "recipeStep": recipeStep,
#                         "stepNo": stepNo,
#                         "state": state 
#                     }
#                 }
#     return jsonify(res)

#5. 좋아요 싫어요는 서버에서 할게 아니지?

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='ec2-13-125-180-243.ap-northeast-2.compute.amazonaws.com',port=5000)
    # app.run(port=5000)

# #셰프명으로 레시피 랜덤추천
# @app.route("/recommendRecipeByChef", methods=["POST"])
# def recommendRecipeByChef():
#     req = request.json
#     chef = req['action']['parameters']['chef']['value']
#     result = {
#         "recipeId": tmpRecipe["id"],
#         "name": tmpRecipe["name"]
#         }
#     return jsonify(result)

# #레시피에서스텝찾기
# @app.route("/answerStepFromRecipeByStepNo", methods=["POST"])
# def answerStepFromRecipeByStepNo():
#     req = request.json
#     # step = req['action']['parameters']['step']['value']
#     step = 3
#     result = {
#         "recipeId": tmpRecipe["id"],
#         "step": tmpRecipe["steps"][step],
#         "stepNo": step
#         }
#     return jsonify(result)

# #레시피에서재료찾기
# @app.route("/answerFromIngredientsFromRecipe", methods=["POST"])
# def answerFromIngredientsFromRecipe():
#     req = request.json
#     # recipe = req['action']['parameters']['recipe']['value']
#     result = {
#         "recipeId": tmpRecipe["id"],
#         "ingredients": tmpRecipe["ingredients"]
#         }
#     return jsonify(result)
