<script lang="ts">
	import { QueryClient, QueryClientProvider } from '@sveltestack/svelte-query'
	import { userData } from '$lib/store/userStore';
	import { facilitiesData } from '$lib/store/facilityStore';
	import { fly } from 'svelte/transition';
	import {
    Button,
    Card,
    CardBody,
    CardFooter,
    CardHeader,
    CardSubtitle,
    CardText,
    CardTitle
    } from 'sveltestrap';
    import LL from '$i18n/i18n-svelte'
	//export let posts;
	import Ghost from '$lib/Ghost/Ghost.svelte';
	const queryClient = new QueryClient()
</script>

<svelte:head>
	<title>
		Maison de santé de Vedène
	</title>
</svelte:head>

<section in:fly={{ y: -100, duration: 500, delay: 500 }} out:fly={{ duration: 500 }}>
	<div class="container">
		<div class="row align-items-start">
		  <div class="col">
			{$LL.WELCOME()} dans Maison de santé pluriprofessionnelle de Vedène
			{#if $userData.username}
			<span style="text-transform: capitalize;">{$userData.username}</span>{/if}
			!
		  </div>
		  <div class="col">
			<QueryClientProvider client={queryClient}>
			<Ghost />
		    </QueryClientProvider>
		  <div class="col">
			<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cone-striped" viewBox="0 0 16 16">
				<path d="m9.97 4.88.953 3.811C10.159 8.878 9.14 9 8 9c-1.14 0-2.158-.122-2.923-.309L6.03 4.88C6.635 4.957 7.3 5 8 5s1.365-.043 1.97-.12zm-.245-.978L8.97.88C8.718-.13 7.282-.13 7.03.88L6.275 3.9C6.8 3.965 7.382 4 8 4c.618 0 1.2-.036 1.725-.098zm4.396 8.613a.5.5 0 0 1 .037.96l-6 2a.5.5 0 0 1-.316 0l-6-2a.5.5 0 0 1 .037-.96l2.391-.598.565-2.257c.862.212 1.964.339 3.165.339s2.303-.127 3.165-.339l.565 2.257 2.391.598z"/>
			  </svg> Site en construction. Contacter le développeur <a href="/jerome-pinguet">Jérôme Pinguet</a>.
		  </div>
		</div>
</section>
