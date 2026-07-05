import cv2
import folium
import utils

def run_map_interface():
    precision = 64
    mapObj = folium.Map(location=[38.56, 28.01],
                        zoom_start=13)

    predict_start_end_coords_file_path = "./predict_start_end_coordinates.txt"

    start_end_coordinates_file = open(predict_start_end_coords_file_path, "r")
    filenames=[]
    for line in start_end_coordinates_file.readlines():
        filename=line.split(":")[1].rstrip()
        part1=line.split(":")[0]
        part11 = part1.split(";")[0]
        part12 = part1.split(";")[1]
        lonA = float(part11.split(",")[0])
        latB = float(part11.split(",")[1])
        lonB = float(part12.split(",")[0])
        latA = float(part12.split(",")[1])

        folium.Marker(
            location=[latB, lonA],
            popup="PREDICTION IS HERE",
            icon=folium.Icon(icon="info-sign")
        ).add_to(mapObj)

        composite_image = cv2.imread("./"+filename)
        filenames.append("./"+filename)
        composite_image = cv2.cvtColor(composite_image, cv2.COLOR_BGR2RGB)


        for i in range(precision-1):
            for j in range(precision-1):
                currentLonA=lonA+(i*((lonB-lonA)/precision))
                currentLonB=lonA+((i+1)*((lonB-lonA)/precision))
                currentLatA=latA-(j*((latA-latB)/precision))
                currentLatB=latA-((j+1)*((latA-latB)/precision))

                color = composite_image[63-j][i]

                folium.Polygon([
                    (currentLatB, currentLonA),
                    (currentLatB, currentLonB),
                    (currentLatA, currentLonB),
                    (currentLatA, currentLonA)
                    ],
                       stroke=False,
                       color="#a632a8",
                       weight=2,
                       fill=True,
                       fill_color="#{:02x}{:02x}{:02x}".format(*color),
                       fill_opacity=1).add_to(mapObj)

    legend_html = '''
    <div style="
        position: fixed; 
        bottom: 50px; left: 50px; width: 200px; height: auto; 
        border:2px solid grey; z-index:9999; font-size:14px;
        background-color:white; padding: 10px;
        ">
        <b>Legend</b> <br>
        <i class="fa fa-map-marker fa-2x" style="color:rgb(255,149,0)"></i>&nbsp;Buğday<br>
        <i class="fa fa-map-marker fa-2x" style="color:rgb(212,255,0)"></i>&nbsp;Domates<br>
        <i class="fa fa-map-marker fa-2x" style="color:rgb(64,255,0)"></i>&nbsp;Mısır<br>
        <i class="fa fa-map-marker fa-2x" style="color:rgb(0,255,234)"></i>&nbsp;Mısır2<br>
        <i class="fa fa-map-marker fa-2x" style="color:rgb(0,127,255)"></i>&nbsp;Pamuk<br>
        <i class="fa fa-map-marker fa-2x" style="color:rgb(21,0,255)"></i>&nbsp;Üzüm<br>
        <i class="fa fa-map-marker fa-2x" style="color:rgb(255,0,191)"></i>&nbsp;Yonca<br>
        <i class="fa fa-map-marker fa-2x" style="color:rgb(255,0,43)"></i>&nbsp;Zeytin<br>
        <i class="fa fa-map-marker fa-2x" style="color:rgb(170,170,170)"></i>&nbsp;Tarım Dışı Alan<br>
    </div>
    '''

    mapObj.get_root().html.add_child(folium.Element(legend_html))

    mapObj.save('output.html')

    start_end_coordinates_file.close()
    utils.delete_file_if_exists(predict_start_end_coords_file_path)
    for file_to_delete in filenames:
        utils.delete_file_if_exists(file_to_delete)

    print("Check output.html on browser...")

