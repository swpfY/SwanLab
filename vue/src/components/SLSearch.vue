<template>
  <div class="w-full border flex gap-2 justify-between items-center py-2 px-2 rounded-lg">
    <SLIcon class="w-4 h-4 shrink-0" icon="search"></SLIcon>
    <input
      type="text"
      v-model="value"
      class="w-full outline-none text-xs text-dimmer"
      :placeholder="placeholder"
      @input="input"
      @keydown.enter="$emit('search', value)"
    />
  </div>
</template>

<script setup>
/**
 * @description: 搜索
 * @file: SLSearch.vue
 * @since: 2024-01-08 16:36:14
 **/

import { ref } from 'vue'
import SLIcon from './SLIcon.vue'
import { debounce } from '@swanlab-vue/utils/common'
import { t } from '@swanlab-vue/i18n'

const emits = defineEmits(['input', 'search'])

const props = defineProps({
  dealy: {
    type: String,
    default: '500'
  },
  placeholder: {
    type: String,
    default: t('common.search.placeholder')
  }
})

const value = ref('')

const input = debounce(() => {
  emits('input', value.value)
}, props.dealy)
</script>

<style lang="scss" scoped></style>
