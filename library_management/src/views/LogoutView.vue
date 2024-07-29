<script setup>
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
// import { }f

const message_store = messageStore();
const auth_store = auth();

const router = useRouter();

auth_store.logout().then(
    (resp)=>{
        message_store.setmessage(resp.message)
        console.log(resp)
        router.push({path: '/'})
        // console.log($parent)
    }
)

</script>