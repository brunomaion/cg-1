import tkinter as tk
from tkinter import colorchooser

class ponto:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.cor = color

    def xy(self):
        return (self.x, self.y)
    
class Triangle:
    def __init__(self, id):
        self.pontos = []
        self.id = id

class app:
    def __init__(self, root):
        self.root = root
        self.root.title("Triângulo")
        self.canvas = tk.Canvas(root, width=800, height=800, bg="white")
        self.canvas.pack()
        self.vertices = []
        self.canvas.bind("<Button-1>", self.addVert)

    def addVert(self, event):
        x, y = event.x, event.y
        cor = colorchooser.askcolor()[1]
        self.vertices.append(ponto(x, y, cor))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=cor)
        if len(self.vertices) == 3:
            self.desenhar_triangulo()

    def desenhar_triangulo(self):
        triangulo = Triangle(len(self.vertices))
        triangulo.pontos = self.vertices
        self.fill_poly(triangulo)

    def fill_poly(self, triangulo):
        vertices = [(ponto.xy(), ponto.cor) for ponto in triangulo.pontos]

        def interpolar(color1, color2, color3, t1, t2, t3):
            r = int(t1 * color1[0] + t2 * color2[0] + t3 * color3[0])
            g = int(t1 * color1[1] + t2 * color2[1] + t3 * color3[1])
            b = int(t1 * color1[2] + t2 * color2[2] + t3 * color3[2])
            r = max(0, min(r, 255))
            g = max(0, min(g, 255))
            b = max(0, min(b, 255))
            return r, g, b

        def hex2rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def rgb2hex(rgb):
            return f'#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'

        minY = min(vertices, key=lambda p: p[0][1])[0][1]
        maxY = max(vertices, key=lambda p: p[0][1])[0][1]

        for y in range(minY, maxY + 1):
            intersections = []

            for i in range(3):
                x1, y1 = vertices[i][0]
                x2, y2 = vertices[(i + 1) % 3][0]
                if y1 <= y + 1e-6 <= y2 or y2 <= y + 1e-6 <= y1:
                    if y2 - y1 != 0:
                        x = int(x1 + (y + 1e-6 - y1) * (x2 - x1) / (y2 - y1))
                        intersections.append(x)

            intersections.sort()

            for i in range(0, len(intersections), 2):
                x1 = intersections[i]
                x2 = intersections[i + 1] if i + 1 < len(intersections) else intersections[0]

                for x in range(x1, x2 + 1):
                    d = [((vx - x) ** 2 + (vy - y) ** 2) ** 0.5 for ((vx, vy), _) in vertices]
                    total = sum(1 / ((di + 1e-6) ** 2) for di in d)
                    t = [(1 / ((di + 1e-6) ** 2)) / total for di in d]

                    color1 = hex2rgb(vertices[0][1])
                    color2 = hex2rgb(vertices[1][1])
                    color3 = hex2rgb(vertices[2][1])

                    color = interpolar(color1, color2, color3, t[0], t[1], t[2])
                    color_hex = rgb2hex(color)

                    self.canvas.create_line(x, y, x + 1, y, fill=color_hex)

if __name__ == "__main__":
    root = tk.Tk()
    app = app(root)
    root.mainloop()
