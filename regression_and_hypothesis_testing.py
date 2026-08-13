import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# ======================
# 1. 读取数据
# ======================
df = pd.read_excel("final_dataset.xlsx")

# ======================
# 2. 清洗 Type
# ======================
df['Type'] = df['Type'].str.lower().str.strip()
df = df[df['Type'].isin(['intragroup', 'intergroup', 'outergroup'])]

# ======================
# 3. 数值变量
# ======================
for col in ['Assertiveness', 'Cooperativeness', 'Average Emotion']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['Assertiveness', 'Cooperativeness', 'Average Emotion', 'subreddit'])

df[['Assertiveness', 'Cooperativeness']] = scaler.fit_transform(
    df[['Assertiveness', 'Cooperativeness']]
)

# ======================
# 4. 构造 dummy
# ======================
dummies = pd.get_dummies(df['Type'], prefix='D').astype(int)
df = pd.concat([df, dummies], axis=1)

# ======================
# 5. interaction（partition LSDV 核心）
# ======================
for t in ['intragroup', 'intergroup', 'outergroup']:
    df[f'A_{t}'] = df['Assertiveness'] * df[f'D_{t}']
    df[f'C_{t}'] = df['Cooperativeness'] * df[f'D_{t}']

# ======================
# 6. 设计矩阵
# ======================
X = df[
    ['D_intragroup', 'D_intergroup', 'D_outergroup',
     'A_intragroup', 'A_intergroup', 'A_outergroup',
     'C_intragroup', 'C_intergroup', 'C_outergroup']
]

y = df['Average Emotion']

X = X.astype(float)
y = y.astype(float)

# ======================
# 7. OLS + cluster robust SE
# ======================
model = sm.OLS(y, X).fit(
    cov_type='cluster',
    cov_kwds={'groups': df['subreddit']}
)

print(model.summary())

# ======================
# 8. Wald tests / coefficient comparison
# ======================
print("\n" + "="*70)
print("WALD TESTS: COEFFICIENT DIFFERENCES ACROSS CONFLICT TYPES")
print("="*70)

# ---- A (Assertiveness) slope comparisons ----
print("\n[1] Compare Assertiveness slopes across groups")
print("\nH0: A_intragroup = A_intergroup")
print(model.t_test("A_intragroup = A_intergroup"))

print("\nH0: A_intragroup = A_outergroup")
print(model.t_test("A_intragroup = A_outergroup"))

print("\nH0: A_intergroup = A_outergroup")
print(model.t_test("A_intergroup = A_outergroup"))

# ---- C (Cooperativeness) slope comparisons ----
print("\n[2] Compare Cooperativeness slopes across groups")
print("\nH0: C_intragroup = C_intergroup")
print(model.t_test("C_intragroup = C_intergroup"))

print("\nH0: C_intragroup = C_outergroup")
print(model.t_test("C_intragroup = C_outergroup"))

print("\nH0: C_intergroup = C_outergroup")
print(model.t_test("C_intergroup = C_outergroup"))

# ---- Intercept comparisons ----
print("\n[3] Compare group intercepts across conflict types")
print("\nH0: D_intragroup = D_intergroup")
print(model.t_test("D_intragroup = D_intergroup"))

print("\nH0: D_intragroup = D_outergroup")
print(model.t_test("D_intragroup = D_outergroup"))

print("\nH0: D_intergroup = D_outergroup")
print(model.t_test("D_intergroup = D_outergroup"))

# ======================
# 9. Joint Wald tests
# ======================
print("\n" + "="*70)
print("JOINT WALD TESTS")
print("="*70)

# A slopes jointly equal across all groups
print("\nH0: A_intragroup = A_intergroup = A_outergroup")
print(model.f_test([
    "A_intragroup = A_intergroup",
    "A_intergroup = A_outergroup"
]))

# C slopes jointly equal across all groups
print("\nH0: C_intragroup = C_intergroup = C_outergroup")
print(model.f_test([
    "C_intragroup = C_intergroup",
    "C_intergroup = C_outergroup"
]))

# Intercepts jointly equal across all groups
print("\nH0: D_intragroup = D_intergroup = D_outergroup")
print(model.f_test([
    "D_intragroup = D_intergroup",
    "D_intergroup = D_outergroup"
]))