<script setup>
import DetailHot from "./components/DetailHot.vue";
import { getDetail } from "@/apis/detail";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { ElMessage } from "element-plus";
import { useCartStore } from "@/stores/cartStore";
const cartStore = useCartStore();
const goods = ref({});
const route = useRoute();
const getGoods = async () => {
  try {
    const res = await getDetail(route.params.id);
    if (res && res.result) {
      goods.value = res.result;
      console.log(res.result);
    } else {
      ElMessage.error("商品数据获取失败");
    }
  } catch (error) {
    ElMessage.error("请求出错，请稍后再试");
    console.error(error);
  }
};

onMounted(() => {
  if (route.params.id) {
    getGoods();
  } else {
    ElMessage.warning("缺少商品ID");
  }
});

// sku规格被操作时
let skuObj = {};
const skuChange = (sku) => {
  console.log(sku);
  skuObj = sku;
};

// count
const count = ref(1);
const countChange = (count) => {
  console.log(count);
};

// 添加购物车
const addCart = () => {
  if (count) {

    // 规则已经选择  触发action
    cartStore.addCart({
      id: goods.value.id,
      name: goods.value.name,
      picture: goods.value.picture,
      price: goods.value.price,
      count: count.value,
      // attrsText: skuObj.specsText,
      selected: true,
    });
    console.log("要添加的商品", goods);
    ElMessage.success("添加购物车成功");
  } else {
    // 规格没有选择 提示用户
    ElMessage.warning("请选择数量");
  }
};
</script>

<template>
  <div class="xtx-goods-page">
    <div class="container" v-if="goods.details">
      <!-- 面包屑 -->
      <div class="bread-container">
        <el-breadcrumb separator=">">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item
            v-if="goods.categories && goods.categories[0].parent"
            :to="{ path: `/category/${goods.categories[0]?.parent.id}` }"
            >{{ goods.categories[0]?.parent.name }}
          </el-breadcrumb-item>
          <el-breadcrumb-item
            v-if="goods.categories && goods.categories[0]"
            :to="{ path: `/category/sub/${goods.categories[0]?.id}` }"
            >{{ goods.categories[0]?.name }}
          </el-breadcrumb-item>
          <el-breadcrumb-item>{{ goods.name }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
      <!-- 商品信息 -->
      <div class="info-container">
        <div>
          <div class="goods-info">
            <div class="media">
              <!-- 图片预览区 -->
              <img :src="goods.mainPictures" class="picture" alt="Product Image" />
              <!-- 统计数量 -->
              <ul class="goods-sales">
                <li>
                  <p>{{ goods.salesCount }}+</p>
                  <p><i class="iconfont icon-task-filling"></i>本书销量</p>
                </li>
                <li>
                  <p>{{ goods.commentCount }}+</p>
                  <p><i class="iconfont icon-comment-filling"></i>评价数量</p>
                </li>
                <li>
                  <p>{{ goods.collectCount }}+</p>
                  <p><i class="iconfont icon-favorite-filling"></i>收藏数量</p>
                </li>
                <li>
                  <p class="brand">{{ goods.brand?.name }}</p>
                  <p><i class="iconfont icon-dynamic-filling"></i>出版社</p>
                </li>
              </ul>
            </div>
            <div class="spec">
              <!-- 商品信息区 -->
              <p class="g-name">{{ goods.name }}</p>
              <p class="g-desc">{{ goods.desc }}</p>
              <p class="g-price">
                <span>{{ goods.price }}</span>
                <span> {{ goods.oldPrice }}</span>
              </p>
              <div class="g-service">
                <dl>
                  <dt>促销</dt>
                  <dd>12月好物放送，App领券购买直降120元</dd>
                </dl>
                <dl>
                  <dt>服务</dt>
                  <dd>
                    <span>无忧退货</span>
                    <span>快速退款</span>
                    <span>免费包邮</span>
                  </dd>
                </dl>
              </div>
              <!-- sku组件 -->
              <XtxSku :goods="goods" @change="skuChange" />
              <!-- 数据组件 -->
              <el-input-number v-model="count" @change="countChange" />
              <!-- 按钮组件 -->
              <div>
                <el-button size="large" class="btn" @click="addCart">
                  加入购物车
                </el-button>
              </div>
            </div>
          </div>
          <div class="goods-footer">
            <div class="goods-article">
              <!-- 商品详情 -->
              <div class="goods-tabs">
                <nav>
                  <a>商品详情</a>
                </nav>
                <div class="goods-detail">
                  <!-- 属性 -->
                  <ul class="attrs">
                    <li
                      v-for="item in goods.details.properties"
                      :key="item.value"
                    >
                      <span class="dt">{{ item.name }}</span>
                      <span class="dd">{{ item.value }}</span>
                    </li>
                  </ul>
                  <!-- 图片 -->
                  <img
                    v-for="img in goods.details.pictures"
                    :src="img"
                    :key="img"
                    alt=""
                  />
                </div>
              </div>
            </div>
            <!-- 24热榜+专题推荐 -->
            <!--<div class="goods-aside">-->
            <!--  &lt;!&ndash; 24小时 &ndash;&gt;-->
            <!--  <DetailHot :hot-type="1" />-->
            <!--  &lt;!&ndash; 周 &ndash;&gt;-->
            <!--  <DetailHot :hot-type="2" />-->
            <!--</div>-->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.xtx-goods-page {
  .goods-info {
    min-height: 600px;
    background: #fff;
    display: flex;

    .media {
      width: 580px;
      height: 600px;
      padding: 30px 50px;

      .picture {
        height: 80%;
        object-fit: cover;
      }
    }

    .spec {
      flex: 1;
      padding: 30px 30px 30px 0;
    }
  }

  .goods-footer {
    display: flex;
    margin-top: 20px;

    .goods-article {
      width: 940px;
      margin-right: 20px;
    }

    .goods-aside {
      width: 280px;
      min-height: 1000px;
    }
  }

  .goods-tabs {
    min-height: 600px;
    background: #fff;
  }

  .goods-warn {
    min-height: 600px;
    background: #fff;
    margin-top: 20px;
  }

  .number-box {
    display: flex;
    align-items: center;

    .label {
      width: 60px;
      color: #999;
      padding-left: 10px;
    }
  }

  .g-name {
    font-size: 22px;
  }

  .g-desc {
    color: #999;
    margin-top: 10px;
    width: 80%;

  }

  .g-price {
    margin-top: 10px;

    span {
      &::before {
        content: "¥";
        font-size: 14px;
      }

      &:first-child {
        color: $priceColor;
        margin-right: 10px;
        font-size: 22px;
      }

      &:last-child {
        color: #999;
        text-decoration: line-through;
        font-size: 16px;
      }
    }
  }

  .g-service {
    background: #f5f5f5;
    width: 500px;
    padding: 20px 10px 0 10px;
    margin-top: 10px;

    dl {
      padding-bottom: 20px;
      display: flex;
      align-items: center;

      dt {
        width: 50px;
        color: #999;
      }

      dd {
        color: #666;

        &:last-child {
          span {
            margin-right: 10px;

            &::before {
              content: "•";
              color: $theme;
              margin-right: 2px;
            }
          }

          a {
            color: $theme;
          }
        }
      }
    }
  }

  .goods-sales {
    display: flex;
    width: 400px;
    align-items: center;
    text-align: center;
    height: 140px;

    li {
      flex: 1;
      position: relative;

      ~ li::after {
        position: absolute;
        top: 0px;
        left: 0;
        height: 60px;
        border-left: 1px solid #e4e4e4;
        content: "";
      }

      p {
        &:first-child {
          color: #999;
        }

        &:nth-child(2) {
          color: $priceColor;
          margin-top: 10px;
        }

        &:last-child {
          color: #666;
          margin-top: 10px;

          i {
            color: $theme;
            font-size: 14px;
            margin-right: 2px;
          }

          &:hover {
            color: $theme;
            cursor: pointer;
          }
        }
      }
    }
  }
}

.goods-tabs {
  min-height: 600px;
  background: #fff;

  nav {
    height: 70px;
    line-height: 70px;
    display: flex;
    border-bottom: 1px solid #f5f5f5;

    a {
      padding: 0 40px;
      font-size: 18px;
      position: relative;

      > span {
        color: $priceColor;
        font-size: 16px;
        margin-left: 10px;
      }
    }
  }
}

.goods-detail {
  padding: 40px;

  .attrs {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 30px;

    li {
      display: flex;
      margin-bottom: 10px;
      width: 50%;

      .dt {
        width: 100px;
        color: #999;
      }

      .dd {
        flex: 1;
        color: #666;
      }
    }
  }

  > img {
    width: 100%;
  }
}

.btn {
  margin-top: 20px;
}

.bread-container {
  padding: 25px 0;
}

.brand {
  width:max-content;
}
</style>
