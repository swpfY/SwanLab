<template>
  <div class="w-full" v-if="requirements">
    <template v-if="requirements.length !== 0">
      <!-- 搜索、复制、下载 -->
      <FuncBar
        class="pb-6 py-4"
        @input="search"
        :content="requirements?.join('\n')"
        :filename="filename"
        :placeholder="$t('experiment.func-bar.placeholder.requirements')"
      />
      <!-- 如果有依赖项 -->
      <div class="px-6 py-4 bg-higher rounded">
        <p v-for="line in lines" :key="line">
          <span v-show="!line.isTarget">{{ line.value }}</span>
          <span v-show="line.isTarget">
            <span
              v-for="substring in line.value"
              :key="substring"
              :class="substring.toLowerCase() === searchValue ? ' bg-warning-dimmest' : ''"
            >
              {{ substring }}
            </span>
          </span>
        </p>
      </div>
    </template>
    <!-- 没有依赖项时占位 -->
    <div class="w-full flex flex-wrap justify-center pt-10" v-else>
      <SLIcon class="magnifier" icon="search"></SLIcon>
      <div class="font-semibold w-full text-center pt-10">{{ $t('experiment.env.empty.requirements') }}</div>
    </div>
  </div>
</template>

<script setup>
/**
 * @description: 依赖项
 * @file: EnvDependances.vue
 * @since: 2024-01-09 16:01:55
 **/

import { ref, computed } from 'vue'
import { useExperimentStroe } from '@swanlab-vue/store'
import FuncBar from '@swanlab-vue/views/experiment/components/FuncBar.vue'
import http from '@swanlab-vue/api/http'

const experimentStore = useExperimentStroe()
const requirements = ref()

http
  .get(`/experiment/${experimentStore.id}/requirements`)
  .then(({ data }) => {
    requirements.value = data.requirements
  })
  .catch(() => {
    requirements.value = []
  })

// ---------------------------------- 搜索 ----------------------------------

// 查找字符
const searchValue = ref('')

const search = (value) => {
  searchValue.value = value.toLowerCase().trim()
}

// 对依赖的每一行进行一些特殊处理
const lines = computed(() => {
  return requirements.value.map((line) => {
    // 查找内容不为空，并且该行含有查找内容，说明是目标行
    const isTarget = searchValue.value !== '' && line.toLowerCase().includes(searchValue.value)

    return {
      isTarget,
      value: isTarget ? splitStringBySearch(line, searchValue.value) : line
    }
  })
})

// 以查找字符串作为分割点，将一行字符串分割成数组，且忽略大小写
function splitStringBySearch(target, substring) {
  // 使用正则表达式进行大小写不敏感的分割，并保留分割点
  let resultArray = target.split(new RegExp(`(${substring})`, 'i'))

  // 去除数组中的空字符串
  resultArray = resultArray.filter((item) => item !== '')

  // 返回包含分割点的数组
  return resultArray
}

// ---------------------------------- 下载成文件 ----------------------------------

const filename = 'requirements.txt'
</script>

<style lang="scss" scoped>
$duration: 3s;

.magnifier {
  @apply w-10 h-10;
  animation: animloader $duration infinite;
}

@keyframes animloader {
  0% {
    transform: translate(-5px, -5px);
  }
  25% {
    transform: translate(-5px, 5px);
  }
  50% {
    transform: translate(5px, 5px);
  }
  75% {
    transform: translate(5px, -5px);
  }
  100% {
    transform: translate(-5px, -5px);
  }
}
</style>
