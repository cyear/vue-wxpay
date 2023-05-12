<script setup>
import { ref,reactive } from 'vue';
import { showToast } from '@nutui/nutui';
import '@nutui/nutui/dist/packages/toast/style';
import axios from 'axios';


const id = ref(window.location.hash.split('?')[1].split('=')[1])

const formData = reactive({
  name: '',
  tel: '',
  address: '',
  remarks: '',
  id: null,
});

const ruleForm = ref(null);

const submit = () => {
  ruleForm.value.validate().then(({ valid, errors }) => {
    if (valid) {
      formData.id = id
      console.log('success', formData);
      // 发送 POST 请求
      axios.post('/api/buy', formData).then(response => {
        console.log(response.data);
        window.location.href=response.data;
        //document.getElementById("buy").innerHTML = response.data
        // 在这里处理后端返回的字符串
      }).catch(error => {
        console.error(error);
      });
    } else {
      console.log('error submit!!', errors);
    }
  });
};

/*const reset = () => {
  ruleForm.value.reset();
};*/

const customBlurValidate = (prop) => {
  ruleForm.value.validate(prop).then(({ valid, errors }) => {
    if (valid) {
      console.log('success', formData);
    } else {
      console.log('error submit!!', errors);
    }
  });
};

//const customValidator = (val) => /^\d+$/.test(val);

/*const customRulePropValidator = (val, rule) => {
  return (rule?.reg).test(val);
};*/

const nameLengthValidator = (val) => val?.length >= 2;

const asyncValidator = (val) => {
  return new Promise((resolve) => {
    showToast.loading('创建订单信息...');
    setTimeout(() => {
      showToast.hide();
      resolve(/^400(-?)[0-9]{7}$|^1\d{10}$|^0[0-9]{2,3}-[0-9]{7,8}$/.test(val));
    }, 1000);
  });
};

</script>

<template>

  <nut-navbar @on-click-back="back" @on-click-title="title" title="订单详情">
    <template #left>
      <a href="#/" style="text-decoration: none;">返回</a>
    </template>
    <template #right>
      <ShareN width="16px"></ShareN>
    </template>
  </nut-navbar>
  <div id="buy">
    <p>当前购买的商品 ID 是 {{ id }}</p>
  </div>


<nut-form :model-value="formData" :rules="{name: [{
            message: 'name 至少两个字符',
            validator: nameLengthValidator
          }]}" ref="ruleForm">
  <nut-form-item label="姓名" prop="name" required :rules="[{ required: true, message: '请填写姓名' }]">
    <nut-input class="nut-input-text" @blur="customBlurValidate('name')" v-model="formData.name"
      placeholder="请输入姓名" type="text" />
  </nut-form-item>
  <nut-form-item label="联系电话" prop="tel" required :rules="[
      { required: true, message: '请填写联系电话' },
      { validator: asyncValidator, message: '电话格式不正确' }
    ]">
    <nut-input class="nut-input-text" v-model="formData.tel" placeholder="请输入联系电话" type="text" />
  </nut-form-item>
  <nut-form-item label="地址" prop="address" required :rules="[{ required: true, message: '请填写地址' }]">
    <nut-input class="nut-input-text" v-model="formData.address" placeholder="请输入地址" type="text" />
  </nut-form-item>
  <nut-form-item label="备注">
    <nut-textarea  v-model="formData.remarks" placeholder="请输入备注" type="text" />
  </nut-form-item>
  <nut-cell>
    <nut-button type="primary" size="small" style="margin-right: 10px" @click="submit">提交订单</nut-button>
    <!--nut-button size="small" @click="reset">重置提示状态</nut-button-->
  </nut-cell>
</nut-form>

</template>