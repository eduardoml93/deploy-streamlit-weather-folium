import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# Desativar a observação de arquivos para o Streamlit no Docker
# st.set_option('server.headless', True)

# Chave de API da OpenWeatherMap (substitua pela sua chave)
API_KEY = "a5676ce9dbe81f9ddad2125c4dedb9b6"

def obter_previsao_tempo(cidade):
    endpoint = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric"  # Use "imperial" para Fahrenheit ou "metric" para Celsius
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        dados_clima = response.json()
        return dados_clima
    else:
        st.error(f"Erro ao obter dados de previsão do tempo. Código de status: {response.status_code}")
        return None

def exibir_previsao_tempo(dados_clima):
    if dados_clima:
        st.write(f"**Cidade:** {dados_clima['name']}")
        st.write(f"**País:** {dados_clima['sys']['country']}")
        st.write(f"**Temperatura Atual:** {dados_clima['main']['temp']}°C")
        st.write(f"**Tempo:** {dados_clima['weather'][0]['description'].capitalize()}")
        return dados_clima
    else:
        st.warning("Insira uma cidade válida.")
        return None

def exibir_mapa(latitude, longitude, dados_clima):
    st.write("**Mapa da Cidade**")
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    
    # Adicione informações sobre o clima no pop-up do marcador
    pop_up_content = f"""
    <b>Cidade:</b> {dados_clima['name']}<br>
    <b>País:</b> {dados_clima['sys']['country']}<br>
    <b>Temperatura Atual:</b> {dados_clima['main']['temp']}°C<br>
    <b>Tempo:</b> {dados_clima['weather'][0]['description'].capitalize()}
    """
    
    folium.Marker(location=[latitude, longitude], popup=folium.Popup(html=pop_up_content, parse_html=True)).add_to(m)
    folium_static(m)

def main():
    st.title("App de Previsão do Tempo e Mapa")

    # Inserir o nome da cidade
    cidade = st.text_input("Digite o nome da cidade:")

    # Botão para obter a previsão do tempo
    if st.button("Obter Previsão do Tempo"):
        if cidade:
            dados_clima = obter_previsao_tempo(cidade)
            if dados_clima:
                coordenadas = exibir_previsao_tempo(dados_clima)
                exibir_mapa(*coordenadas, dados_clima)
        else:
            st.warning("Insira o nome da cidade para obter a previsão do tempo.")

if __name__ == "__main__":
    main()




