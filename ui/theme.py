import streamlit as st


def load_theme():

    st.markdown("""

<style>

/* ==========================================================
   GOOGLE FONT
========================================================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');


/* ==========================================================
   DESIGN TOKENS
========================================================== */

:root{

    --bg:#f9f4ef;

    --surface:#ffffff;

    --headline:#020826;

    --paragraph:#716040;

    --primary:#8c7851;

    --secondary:#eaddcf;

    --accent:#f25042;

    --border:#ece6de;

    --shadow-sm:
    0 4px 12px rgba(0,0,0,.05);

    --shadow-md:
    0 10px 30px rgba(0,0,0,.08);

    --radius-sm:14px;

    --radius-md:20px;

    --radius-lg:28px;
}


/* ==========================================================
   RESET
========================================================== */

*{

    font-family:'Inter',sans-serif;
}


.stApp{

    background:var(--bg);

    color:var(--headline);
}


/* ==========================================================
   HIDE STREAMLIT IDENTITY
========================================================== */

#MainMenu{

    visibility:hidden;
}



footer{

    visibility:hidden;
}

button[kind="header"]{

    display:none;
}


/* ==========================================================
   PAGE CONTAINER
========================================================== */

.block-container{

    max-width:1280px;

    padding-top:100px;

    padding-left:3rem;

    padding-right:3rem;

    padding-bottom:4rem;
}


/* ==========================================================
   TYPOGRAPHY
========================================================== */

h1{

    color:var(--headline);

    font-size:52px;

    font-weight:800;

    line-height:1.15;
}

h2{

    color:var(--headline);

    font-size:34px;

    font-weight:700;

    line-height:1.2;
}

h3{

    color:var(--headline);

    font-size:24px;

    font-weight:700;
}

p{

    color:var(--paragraph);

    line-height:1.8;
}

.page-title{

    font-size:52px;

    font-weight:800;

    margin-bottom:12px;
}

.section-title{

    font-size:34px;

    font-weight:700;

    margin-bottom:24px;
}

.page-subtitle{

    font-size:18px;

    color:var(--paragraph);

    line-height:1.8;
}


/* ==========================================================
   HERO
========================================================== */

.hero-card{

    background:linear-gradient(

        135deg,

        #ffffff,

        #f5efe8

    );

    border:1px solid var(--border);

    border-radius:var(--radius-lg);

    padding:60px;

    margin-bottom:40px;

    box-shadow:var(--shadow-sm);
}


/* ==========================================================
   CONTENT CARD
========================================================== */

.dashboard-card{

    background:var(--surface);

    border:1px solid var(--border);

    border-radius:var(--radius-md);

    padding:32px;

    margin-bottom:28px;

    box-shadow:var(--shadow-sm);

    transition:.25s ease;
}

.dashboard-card:hover{

    transform:translateY(-4px);

    box-shadow:var(--shadow-md);
}


/* ==========================================================
   STATS CARD
========================================================== */

.metric-card{

    background:var(--surface);

    border:1px solid var(--border);

    border-radius:var(--radius-md);

    min-height:170px;

    padding:28px;

    text-align:center;

    display:flex;

    flex-direction:column;

    justify-content:center;

    box-shadow:var(--shadow-sm);

    transition:.25s ease;
}

.metric-card:hover{

    transform:translateY(-5px);

    box-shadow:var(--shadow-md);
}

.metric-title{

    color:var(--paragraph);

    font-size:14px;

    margin-bottom:14px;

    font-weight:600;
}

.metric-value{

    font-size:38px;

    font-weight:800;

    color:var(--headline);
}


/* ==========================================================
   CHART CARD
========================================================== */

.chart-card{

    background:var(--surface);

    border:1px solid var(--border);

    border-radius:var(--radius-md);

    padding:28px;

    margin-bottom:30px;

    box-shadow:var(--shadow-sm);

    transition:.25s ease;
}

.chart-card:hover{

    transform:translateY(-4px);

    box-shadow:var(--shadow-md);
}

.chart-title{

    font-size:22px;

    font-weight:700;

    color:var(--headline);

    margin-bottom:18px;
}


/* ==========================================================
   USER CARD
========================================================== */

.user-card{

    background:var(--secondary);

    border-radius:16px;

    padding:18px;

    margin-bottom:20px;
}


/* ==========================================================
   BUTTONS
========================================================== */

.stButton>button{

    background:var(--primary);

    color:white;

    border:none;

    border-radius:16px;

    height:52px;

    font-size:16px;

    font-weight:700;

    transition:.25s ease;
}

.stButton>button:hover{

    background:#7a6947;

    transform:translateY(-2px);
}


/* ==========================================================
   PAGE LINKS
========================================================== */

[data-testid="stPageLink"] a{

    background:var(--surface);

    border:1px solid var(--border);

    border-radius:16px;

    padding:16px;

    transition:.25s ease;
}

[data-testid="stPageLink"] a:hover{

    background:var(--secondary);

    transform:translateY(-2px);
}


/* ==========================================================
   INPUTS
========================================================== */

.stTextInput input{

    background:white !important;

    border:1px solid var(--border) !important;

    border-radius:16px !important;

    color:var(--headline) !important;

    height:54px !important;
}


/* ==========================================================
   SELECTBOX
========================================================== */

.stSelectbox{

    margin-bottom:12px;
}


/* ==========================================================
   DATAFRAME
========================================================== */

[data-testid="stDataFrame"]{

    border-radius:18px;

    overflow:hidden;

    border:1px solid var(--border);
}


/* ==========================================================
   PROGRESS BAR
========================================================== */

.stProgress>div>div{

    background:var(--primary);
}

/* ==========================================
   STICKY HEADER
========================================== */

.app-header{

    position:fixed;

    top:0;

    left:0;

    right:0;

    z-index:999;

    height:80px;

    background:#ffffff;

    border-bottom:1px solid var(--border);

    display:flex;

    justify-content:space-between;

    align-items:center;

    padding:0 60px;

    box-shadow:var(--shadow-sm);
}

.header-left{

    display:flex;

    align-items:center;

    gap:16px;
}

.logo-circle{

    width:52px;

    height:52px;

    border-radius:50%;

    background:var(--secondary);

    display:flex;

    align-items:center;

    justify-content:center;

    font-size:24px;
}

.brand-name{

    font-size:22px;

    font-weight:800;

    color:var(--headline);
}

.brand-subtitle{

    font-size:13px;

    color:var(--paragraph);
}

.header-right{

    display:flex;

    align-items:center;

    gap:18px;
}

.notification{

    width:46px;

    height:46px;

    border-radius:50%;

    background:var(--secondary);

    display:flex;

    align-items:center;

    justify-content:center;

    cursor:pointer;
}

.profile-pill{

    padding:12px 20px;

    border-radius:30px;

    background:var(--secondary);

    font-weight:600;
}

.hero-badge{

    display:inline-block;

    padding:10px 18px;

    background:var(--secondary);

    border-radius:30px;

    font-size:14px;

    font-weight:700;

    margin-bottom:22px;
}
.section-heading{

    font-size:38px;

    font-weight:800;

    margin-bottom:30px;
}
.section-banner{

    background:var(--secondary);

    border-radius:16px;

    padding:18px 28px;

    font-size:24px;

    font-weight:700;

    margin-bottom:24px;
}

/* ==========================================================
   FOOTER
========================================================== */

.footer{

    margin-top:100px;

    padding:60px;

    background:#ffffff;

    border-top:1px solid var(--border);

    text-align:center;

    border-radius:28px 28px 0 0;
}


/* ==========================================================
   ANIMATIONS
========================================================== */

@keyframes fadeIn{

    from{

        opacity:0;

        transform:translateY(12px);
    }

    to{

        opacity:1;

        transform:translateY(0);
    }
}

.block-container{

    animation:fadeIn .4s ease;
}

</style>

""", unsafe_allow_html=True)