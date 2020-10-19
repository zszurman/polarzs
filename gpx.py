import math
import tkinter
import webbrowser
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo

import folium
import gpxpy.gpx
from folium import plugins


class Application(Frame):

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.pathLbl = Label(self, text="Nie wybrano pliku gpx", bg="#3E5FA2", fg="white", font=("Calibri", 18))
        self.pathBtn = Button(self, text="Wybierz plik .gpx", command=self.get_file, bg="#3E5FA2", fg="#F5AAAA",
                              font=("Calibri", 18))
        self.htmlLbl = Label(self, text="Wpisz nazwę pliku .html:", bg="#3E5FA2", fg="#F5AAAA", font=("Calibri", 18))
        self.htmlEnt = Entry(self, bg="#CCFFE5", fg="#3E5FA2", font=("Calibri", 18))
        self.htmlEnt.insert(END, "c:/users/zs/downloads/analiza.html")
        self.okBtn = Button(self, text="Kliknij aby wyświetlić mapę", command=self.klik, bg="#3E5FA2", fg="#F5AAAA",
                            font=("Calibri", 18))
        self.storyTxt = Text(self, wrap=WORD, font=("Calibri", 18), bg="#3E5FA2", fg="#00FF00")
        self.pathBtn.grid(row=0, column=0, sticky=N + E + W + S, padx=2, pady=2)
        self.pathLbl.grid(row=0, column=1, sticky=N + E + W + S, padx=2, pady=2)
        self.htmlLbl.grid(row=1, column=0, sticky=N + E + W + S, padx=2, pady=2)
        self.htmlEnt.grid(row=1, column=1, sticky=N + E + W + S, padx=2, pady=2)
        self.storyTxt.grid(row=2, column=0, columnspan=2, padx=2, pady=2)
        self.okBtn.grid(row=3, column=0, sticky=W)
        self.grid()
        self.fileGPX = 'zs.gpx'
        self.fileHTML = 'gg.html'

    def get_file(self):
        fileName = filedialog.askopenfilename(initialdir="c:/users/zs/downloads", title="wybierz plik trasy",
                                              filetypes=(("pliki gpx", "*.gpx"), ("all files", "*.*")))
        self.pathLbl["text"] = fileName

    def gpx_parse(self):
        gpx_file = open(self.fileGPX, 'r')
        return gpxpy.parse(gpx_file)

    def points_x(self):
        gpx = self.gpx_parse()
        points_x = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points_x.append(point.latitude)
        return points_x

    def points_y(self):
        gpx = self.gpx_parse()
        points_y = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points_y.append(point.longitude)
        return points_y

    def points_xy(self):
        gpx = self.gpx_parse()
        points_xy = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points_xy.append(tuple([point.latitude, point.longitude]))
        return points_xy

    def points_time(self):
        gpx = self.gpx_parse()
        points_time = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points_time.append(point.time)
        print(points_time)
        return points_time

    def points_elevation(self):
        gpx = self.gpx_parse()
        points_elevation = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points_elevation.append(point.elevation)
        return points_elevation

    @staticmethod
    def second_time(sekundy):
        h = sekundy // (60 * 60)
        x = sekundy % (60 * 60)
        m = x // 60
        s = x % 60
        str_h = str(h)
        if h < 10:
            str_h = "0" + str_h
        str_m = str(m)
        if m < 10:
            str_m = "0" + str_m
        str_s = str(s)
        if s < 10:
            str_s = "0" + str_s
        return str_h + ":" + str_m + ":" + str_s

    @staticmethod
    def second_tempo(second):
        m = second // 60
        s = second % 60
        str_m = str(m)
        if m < 10:
            str_m = "0" + str_m
        str_s = str(s)
        if s < 10:
            str_s = "0" + str_s
        return str_m + ":" + str_s

    @staticmethod
    def second_day(data):
        x = str(data)
        dgo = (int(x[11]) * 10) + int(x[12]) * 60 * 60
        dmi = (int(x[14]) * 10 + int(x[15])) * 60
        dse = int(x[17]) * 10 + int(x[18])
        return dgo + dmi + dse

    def up_down(self):
        points_elevation = self.points_elevation()
        i = 0
        wzniosy = 0.0
        spadki = 0.0
        while i < len(points_elevation) - 120:
            x = points_elevation[i]
            y = points_elevation[i + 120]
            z = y - x
            if z > 0:
                wzniosy += z
            if z < 0:
                spadki += z
            i += 120
        return "Wzniosy:" + str(wzniosy) + "m \nSpadki:" + str(spadki) + "m \n"

    def max_high(self):
        gpx = self.gpx_parse()
        maks = 0
        godz = 0
        minuta = 0
        for trasa in gpx.tracks:
            for x in trasa.segments:
                for punkt in x.points:
                    if punkt.elevation > maks:
                        maks = punkt.elevation
                        godz = punkt.time.hour
                        minuta = punkt.time.minute
        str_maks = str(int(maks))
        str_godz = str(godz)
        str_minuta = str(minuta)
        if minuta < 10:
            str_minuta = "0" + str_minuta
        return "Maks.wys:" + str_maks + "mnpm\n(godz." + str_godz + ":" + str_minuta + ")\n"

    def start_meta(self):
        points_time = self.points_time()

        t_p = points_time[0]
        d1 = str(t_p.strftime("%Y-%m-%d")) + "\n"
        t1 = "Start:" + str(t_p.strftime("%H:%M")) + "\n"

        t_k = points_time[len(points_time) - 1]
        t2 = "Meta:" + str(t_k.strftime("%H:%M")) + "\n"

        return d1 + t1 + t2

    def all_time_sec(self):
        points_time = self.points_time()
        t_p = points_time[0]
        t_k = points_time[len(points_time) - 1]
        str1 = str(t_p)
        str2 = str(t_k)
        x1 = (int(str2[17]) * 10 + int(str2[18])) - (int(str1[17]) * 10 + int(str1[18]))
        x2 = ((int(str2[14]) * 10 + int(str2[15])) - (int(str1[14]) * 10 + int(str1[15]))) * 60
        x3 = ((int(str2[11]) * 10 + int(str2[12])) - (int(str1[11]) * 10 + int(str1[12]))) * 60 * 60
        x = x1 + x2 + x3
        return x

    def time_pause_sec(self):
        points_time = self.points_time()
        i = 0
        t = 0
        while i < len(points_time) - 1:
            tx = points_time[i]
            x = self.second_day(tx)
            dx = tx.weekday()
            ty = points_time[i + 1]
            y = self.second_day(ty)
            dy = ty.weekday()

            z = y - x
            if z > 1 and dx == dy:
                t += z
                print(z)
            if z > 1 and dx != dy:
                y += 24 * 60 * 60
                z = y - x
                t += z
            i += 1
        return t

    def time_pause_string(self):
        x = self.time_pause_sec()
        return "Postoje:" + self.second_time(x) + "\n"

    def time_ef_string(self):
        x = self.all_time_sec() - self.time_pause_sec()
        return "Ruch:" + self.second_time(x) + "\n"

    def distance_string(self):
        points_x = self.points_x()
        points_y = self.points_y()
        i = 0
        j = 0
        dystans = 0.0
        while i < len(points_x) - 1:
            r = 6373.0
            x1 = points_x[i]
            x2 = points_x[i + 1]
            y1 = points_y[j]
            y2 = points_y[j + 1]
            lat1 = math.radians(x1)
            lat2 = math.radians(x2)
            lon1 = math.radians(y1)
            lon2 = math.radians(y2)
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            dystans += r * c
            i += 1
            j += 1
        return "Dystans:" + str(round(dystans, 2)) + "km\n"

    def distance_km(self):
        points_x = self.points_x()
        points_y = self.points_y()
        i = 0
        j = 0
        dystans = 0.0
        while i < len(points_x) - 1:
            R = 6373.0
            x1 = points_x[i]
            x2 = points_x[i + 1]
            y1 = points_y[j]
            y2 = points_y[j + 1]
            lat1 = math.radians(x1)
            lat2 = math.radians(x2)
            lon1 = math.radians(y1)
            lon2 = math.radians(y2)
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            dystans += R * c
            i += 1
            j += 1
        return dystans

    def speed_string(self):
        t = self.all_time_sec() / 60 / 60
        x = self.distance_km() / t
        return "Vśr.:" + str(round(x, 2)) + "km/h\n"

    def tempo_string(self):
        s = int(self.all_time_sec() / self.distance_km())
        return "Tśr.:" + self.second_tempo(s) + "min/km\n"

    def max_speed_tempo_string(self, deltaMinut):
        points_x = self.points_x()
        points_y = self.points_y()
        i = 0
        j = 0
        record_km = 0
        while i < len(points_x) - deltaMinut * 60:
            r = 6373.0
            x1 = points_x[i]
            x2 = points_x[i + deltaMinut * 60]
            y1 = points_y[j]
            y2 = points_y[j + deltaMinut * 60]
            lat1 = math.radians(x1)
            lat2 = math.radians(x2)
            lon1 = math.radians(y1)
            lon2 = math.radians(y2)
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            x = r * c
            if x > record_km:
                record_km = x
            i += 1
            j += 1
        v_max = round(record_km * 60 / deltaMinut, 2)
        t_sek = int((60 * 60) / v_max)
        return "Vmax(" + str(deltaMinut) + "min).:" + str(v_max) + "km/h\n" + "Tmax(" + str(
            deltaMinut) + "min).:" + self.second_tempo(t_sek) + "min/km\n"

    def max_tempo_string(self, delta_minut):
        points_x = self.points_x()
        points_y = self.points_y()
        i = 0
        j = 0
        record_km = 0
        while i < len(points_x) - delta_minut * 60:
            r = 6373.0
            x1 = points_x[i]
            x2 = points_x[i + delta_minut * 60]
            y1 = points_y[j]
            y2 = points_y[j + delta_minut * 60]
            lat1 = math.radians(x1)
            lat2 = math.radians(x2)
            lon1 = math.radians(y1)
            lon2 = math.radians(y2)
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            x = r * c
            if x > record_km:
                record_km = x
            i += 1
            j += 1
        vMax = round(record_km * 60 / delta_minut, 2)
        tSek = int((60 * 60) / vMax)
        return "Tmax(" + str(delta_minut) + "min).:" + self.second_tempo(tSek) + "min/km\n"

    def __str__(self):
        return "PODSUMOWANIE:\n" + self.start_meta() + self.time_ef_string() + self.time_pause_string() + \
               self.distance_string() + self.speed_string() + self.tempo_string() + self.max_tempo_string(
            1) + self.max_tempo_string(3) + \
               self.max_tempo_string(5) + self.max_tempo_string(6) + self.max_tempo_string(7) + self.max_tempo_string(
            15) + self.up_down() + self.max_high()

    def make_map_and_marker(self):
        self.fileGPX = self.pathLbl["text"]
        self.fileHTML = self.htmlEnt.get()
        story = self
        self.storyTxt.delete(0.0, END)
        self.storyTxt.insert(0.0, story)
        pointsXY = self.points_xy()
        lat = float(sum(p[0] for p in pointsXY) / len(pointsXY))
        lon = float(sum(p[1] for p in pointsXY) / len(pointsXY))
        mapka = folium.Map(location=[lat, lon], zoom_start=13, control_scale=True)
        folium.PolyLine(pointsXY, color="blue", weight=3.5, opacity=1).add_to(mapka)
        folium.CircleMarker(location=[lat, lon], color='none', radius=25, fill_color='blue', popup=self,
                            tooltip=self.fileGPX).add_to(mapka)
        folium.raster_layers.TileLayer('Open Street Map').add_to(mapka)
        folium.raster_layers.TileLayer('StamenTerrain').add_to(mapka)
        folium.raster_layers.TileLayer('CartoDB Positron').add_to(mapka)
        folium.raster_layers.TileLayer('StamenToner').add_to(mapka)
        folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(mapka)
        folium.raster_layers.TileLayer('Stamen Watercolor').add_to(mapka)
        folium.LayerControl().add_to(mapka)
        minimap = plugins.MiniMap(toggle_display=True)
        mapka.add_child(minimap)
        plugins.Fullscreen(position='topright').add_to(mapka)
        measureControl = plugins.MeasureControl(position='topleft', active_color='red', completed_color='red',
                                                primary_length_unit='km')
        mapka.add_child(measureControl)
        draw = plugins.Draw(position='topleft', export='True')
        draw.add_to(mapka)
        mapka.save(self.fileHTML)
        html_page = f'{self.fileHTML}'
        mapka.save(html_page)
        new = 2
        webbrowser.open(html_page, new=new)
        tkinter.messagebox.showinfo("Analiza gpx", "Zakończono analizę pliku i dołączono mapę")

    def klik(self):
        nameGpx = self.pathLbl["text"].lower()
        nameHtml = self.htmlEnt.get()
        if len(nameGpx) < 4:
            nameGpx = "name"
        try:

            if not ".gpx" == (nameGpx[-4:-1] + nameGpx[-1]):
                tkinter.messagebox.showinfo("Analiza gpx", "Wybierz plik .gpx")
            elif not ".html" == (nameHtml[-5:-1] + nameHtml[-1]):
                tkinter.messagebox.showinfo("Analiza gpx", "Wpisz nazwę pliku .html")
            else:
                tkinter.messagebox.showinfo("Analiza gpx", "Analiza pliku może potrwać kilka minut. Rozpocznij analizę")
                self.make_map_and_marker()

        except ZeroDivisionError:
            tkinter.messagebox.showinfo("Analiza gpx", "Wystąpił błąd - dzielenie przez zero")
        except TypeError:
            tkinter.messagebox.showinfo("Analiza gpx", "Wystąpił błąd - niepoprawny typ danych")
        except IndexError:
            tkinter.messagebox.showinfo("Analiza gpx", "Wystąpił błąd - inny")


root = Tk()
Application(root)
root.mainloop()
