import numpy as np

N = 8 #盤面の大きさ
RED = '\033[31m' #色指定
END = '\033[0m'
directions = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)] #8方向探索


class Board:

    def printboard(board): 
        for i in range(N+2):
            for j in range(N+2):

                if (board[i, j] == 1): 
                    print("○", end=" ")
                elif (board[i, j] == 2):
                    print("×", end=" ")
                elif (board[i, j] == 3):
                    print(RED+"-"+END, end=" ") #置けるところを赤色の空白に
                elif (board[i, j] == 4):
                    print("■", end=" ") #外枠を■
                elif (board[i, j] == 0):
                    print("-", end=" ")

            print("")

    def ini(): #初期盤面生成

        board = np.zeros((N+2, N+2)) #numpy配列で盤面を定義
        mid = N // 2
        board[mid, mid+1] = 1
        board[mid+1, mid] = 1
        board[mid, mid] = 2
        board[mid+1, mid+1] = 2

        board[0:10, 0] = 4
        board[0:10, 9] = 4
        board[0, 0:10] = 4
        board[9, 0:10] = 4

        return board

    def range_process(board,player): #ボードのおける範囲を指定

        #ボード上のすべての 3 を 0 にリセット(置ける位置のリセット)
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if board[i, j] == 3:
                    board[i, j] = 0

        #自分と相手を指定
        if player == 1:
            enemy = 2
        else:
            enemy = 1

        #閲覧注意!!4重ループとかいうばけもんがあります
                
        for i in range(1, N + 1): #x座標の探索
            for j in range(1, N + 1): #y座標の探索
                if board[i, j] == 0 : #空いているときのみ
                    for direction in directions: #8方向探索
                        i_direction, j_direction = i + direction[0],j + direction[1] 
                        if 0 <= i_direction < len(board) and 0 <= j_direction < len(board[0]): #壁に当たるまで
                            if board[i_direction,j_direction] == enemy : #敵の駒の場合
                                while 0 <= i_direction < len(board) and 0 <= j_direction < len(board[0]): #壁に当たるまで
                                    i_direction += direction[0] #壁に当たるまで増やしていく
                                    j_direction += direction[1] #壁に当たるまで増やしていく
                                    if board[i_direction, j_direction] == player: #自分と同じ駒なら
                                        board[i, j] = 3 #置ける範囲にする
                                        break
                                    if board[i_direction, j_direction] == 0 or board[i_direction, j_direction] == 4: #何もないもしくは壁なら
                                        break


    def stone_process(board, x, y, player):

        if board[x, y] != 3: #置ける範囲ではない場合
            print("置けません")
            return False
        
        #自分と相手を指定
        if player == 1:
            enemy = 2
        else:
            enemy = 1

        #置けるかどうかのflag
        valid_move = False

        for direction in directions:
            x_direction, y_direction = direction #8方向探索を代入
            x + direction[0],y + direction[1]
            nx, ny = x + x_direction, y + y_direction #探索先の代入
            stones_to_flip = [] #ひっくり返す用の関数を定義
                    
            while 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx, ny] == enemy: #盤の範囲内かつ敵の駒が続くところまで
                stones_to_flip.append((nx, ny)) #append関数で配列に追加
                nx += x_direction #探索をすすめる
                ny += y_direction #探索をすすめる

            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx, ny] == player: #盤の範囲内かつ敵の駒が続くところまで
                valid_move = True #
                for flip_x, flip_y in stones_to_flip: #ひっくり返す配列に代入したのを処理                       
                    board[flip_x, flip_y] = player #ひっくり返す

        if valid_move: 
            board[x, y] = player #置ける場合
            return True
        else: #置けない場合
            print("置けません")
            return False



                

class Player:
    def __init__(self, name, stone):
        self.name = name #プレイヤーの名前の管理
        self.stone = stone #プレイヤーの番号の管理

    def decide_place(self): #入力
        while True:
            try:
                x = int(input(f"{self.name}, x(1-{N}): ")) - 1 #枠の分ずらす
                y = int(input(f"{self.name}, y(1-{N}): ")) - 1
                if 0 <= x < N and 0 <= y < N:
                    return y + 1, x + 1
                else:
                    print(f"1-{N}までの数字を入力してください")
            except ValueError:
                print("整数を入力してください")


class Player1(Player):
    pass


class Player2(Player):
    pass


def main():
    board = Board.ini() #初期化
    player1 = Player1("Player 1", 1) #プレイヤーの数字を設定
    player2 = Player2("Player 2", 2)

    current_player = player1 #プレイヤー1からスタート

    while True: #置けなくなるまで
        Board.range_process(board, current_player.stone) #置ける範囲を探索
        Board.printboard(board) #盤面を表示
        x, y = current_player.decide_place() #駒の座標の入力
        if Board.stone_process(board, x, y, current_player.stone): #駒を置けた場合
            current_player = player2 if current_player == player1 else player1 #プレイヤーの交代

main()