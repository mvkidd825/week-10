# app.py 파일로 저장하고 터미널에서 'streamlit run app.py' 실행

import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# 페이지 설정
st.set_page_config(page_title="Artwork Search", layout="wide")

# 헤더
st.title("🎨 Artwork Search")
st.markdown("Explore artworks from Harvard Art Museums")

# 검색 입력
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input("Search for artworks", placeholder="e.g., painting, portrait, landscape, Monet...", label_visibility="collapsed")
with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

# 검색 실행
if search_button and query:
    with st.spinner("Searching artworks..."):
        try:
            # Harvard Art Museums API
            API_KEY = 'd00d3e90-1e95-11ec-8dd6-d1a56cc297d1'
            url = f'https://api.harvardartmuseums.org/object?apikey={API_KEY}&keyword={query}&hasimage=1&size=12'
            
            response = requests.get(url)
            data = response.json()
            
            if 'records' in data and len(data['records']) > 0:
                st.success(f"✨ Found {len(data['records'])} artworks")
                st.markdown("---")
                
                # 3열 그리드로 표시
                for i in range(0, len(data['records']), 3):
                    cols = st.columns(3)
                    
                    for j in range(3):
                        if i + j < len(data['records']):
                            artwork = data['records'][i + j]
                            
                            with cols[j]:
                                # 이미지 표시
                                if artwork.get('primaryimageurl'):
                                    try:
                                        img_response = requests.get(artwork['primaryimageurl'])
                                        img = Image.open(BytesIO(img_response.content))
                                        st.image(img, use_container_width=True)
                                    except:
                                        st.info("📷 Image not available")
                                else:
                                    st.info("📷 No image")
                                
                                # 작품 정보
                                st.markdown(f"**{artwork.get('title', 'Untitled')}**")
                                
                                # 작가
                                if artwork.get('people') and len(artwork['people']) > 0:
                                    st.text(f"👤 {artwork['people'][0]['name']}")
                                else:
                                    st.text("👤 Unknown Artist")
                                
                                # 날짜
                                if artwork.get('dated'):
                                    st.text(f"📅 {artwork['dated']}")
                                
                                # 매체
                                if artwork.get('medium'):
                                    medium = artwork['medium']
                                    if len(medium) > 60:
                                        medium = medium[:60] + "..."
                                    st.caption(medium)
                                
                                # 링크
                                if artwork.get('url'):
                                    st.markdown(f"[🔗 View at Museum]({artwork['url']})")
                                
                                st.markdown("---")
            else:
                st.warning("⚠️ No artworks found. Try a different search term.")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

elif not query and search_button:
    st.info("💡 Please enter a search term")

else:
    st.info("👆 Enter a search term above and click Search to discover amazing artworks")
    st.markdown("**Try searching for:** painting, sculpture, Rembrandt, Van Gogh, portrait, landscape")
