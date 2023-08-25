<!-- eslint-disable -->
<template>
  <div style="display: flex; flex-direction: column; align-items: center; ">
    <img style="width: 12rem; height: auto;" src="https://raw.githubusercontent.com/baileyg2016/dribbleDigest/main/assets/icon.png" alt="Logo">


    <p class="input-label" style="padding-top: 3rem;">
      What are your favorite sports leagues?
    </p>

    <div @click="isShowingLeagues = !isShowingLeagues" id="leagues" class="text-input" style="cursor: pointer; position: relative; display: flex; flex-direction: row; align-items: center">
      <span class="caption-text" style="color: #747B94; " v-if="data.favoriteLeagues.length === 0">
        Select
      </span>

      <div style="display: flex; flex-direction: row; align-items: center; flex-wrap: wrap;" v-else>
        <span v-for="option in data.favoriteLeagues" style="background-color: #747B94; color: #fff; font-size: 13px; font-weight: 600; border-radius: 6px; padding: .2rem .4rem .2rem .4rem; display: flex; align-items: center; margin: .1rem;">
          {{ option }}

          <svg @click.stop="data.favoriteLeagues = data.favoriteLeagues.filter((other) => option !== other)" style="fill: #fff; width: 1rem; margin-left: .2rem;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12.0007 10.5865L16.9504 5.63672L18.3646 7.05093L13.4149 12.0007L18.3646 16.9504L16.9504 18.3646L12.0007 13.4149L7.05093 18.3646L5.63672 16.9504L10.5865 12.0007L5.63672 7.05093L7.05093 5.63672L12.0007 10.5865Z"></path></svg>
        </span>
      </div>

      <div style="flex-grow: 1;" />

      <svg style="fill: #747B94; width: 20px !important; flex-grow: 0; flex-shrink: 0;" width="20" height="20" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M11.9997 13.1714L16.9495 8.22168L18.3637 9.63589L11.9997 15.9999L5.63574 9.63589L7.04996 8.22168L11.9997 13.1714Z"></path></svg>

      <transition name="grow-fade">
        <div v-if="isShowingLeagues" class="select-dropdown" @click.stop="isShowingLeagues = true">
          <p v-for="option in favoriteLeagueOptions" class="hover-bg" :style="{color: data.favoriteLeagues.includes(option) ? '#FBBCA2' : '#fff'}" style="text-align: left; font-weight: 600; display: flex; justify-content: start; align-items: center;" @click="data.favoriteLeagues = data.favoriteLeagues.includes(option) ? data.favoriteLeagues.filter((other) => other !== option) : [...data.favoriteLeagues, option].slice(0, 5)">
            {{ option }}

            <span style="display: inline-block; flex-grow: 1" />

            <svg v-if="data.favoriteLeagues.includes(option)" style="fill: #FBBCA2; width: 1rem; margin-right: 1.2rem;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22ZM11.0026 16L18.0737 8.92893L16.6595 7.51472L11.0026 13.1716L8.17421 10.3431L6.75999 11.7574L11.0026 16Z"></path></svg>
          </p>
        </div>
      </transition>
    </div>

    <p class="input-label" style="padding-top: 2rem;">
      What are your favorite sports teams?
    </p>

    <div id="teams" @click="isShowingTeams = !isShowingTeams" class="text-input" style="cursor: pointer; position: relative; display: flex; flex-direction: row; align-items: center">
      <span class="caption-text" style="color: #747B94; " v-if="data.favoriteTeams.length === 0">
        Select
      </span>

      <div style="display: flex; flex-direction: row; align-items: center; flex-wrap: wrap;" v-else>
        <span v-for="option in data.favoriteTeams" style="background-color: #747B94; color: #fff; font-size: 13px; font-weight: 600; border-radius: 6px; padding: .2rem .4rem .2rem .4rem; display: flex; align-items: center; margin: .1rem;">
          {{ option }}

          <svg @click.stop="data.favoriteTeams = data.favoriteTeams.filter((other) => option !== other)" style="fill: #fff; width: 1rem; margin-left: .2rem;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12.0007 10.5865L16.9504 5.63672L18.3646 7.05093L13.4149 12.0007L18.3646 16.9504L16.9504 18.3646L12.0007 13.4149L7.05093 18.3646L5.63672 16.9504L10.5865 12.0007L5.63672 7.05093L7.05093 5.63672L12.0007 10.5865Z"></path></svg>
        </span>
      </div>

      <div style="flex-grow: 1;" />

      <svg style="fill: #747B94; width: 20px !important; flex-grow: 0; flex-shrink: 0;" width="20" height="20" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M11.9997 13.1714L16.9495 8.22168L18.3637 9.63589L11.9997 15.9999L5.63574 9.63589L7.04996 8.22168L11.9997 13.1714Z"></path></svg>

      <transition name="grow-fade">
        <div v-if="isShowingTeams" class="select-dropdown" @click.stop="isShowingTeams = true">
          <p v-for="option in query ? favoriteTeamOptions.filter((other) => other.toLowerCase().trim().startsWith(query)) : favoriteTeamOptions" :style="{color: data.favoriteTeams.includes(option) ? '#FBBCA2' : '#fff'}" class="hover-bg" style="text-align: left; font-weight: 600; display: flex; justify-content: start; align-items: center;" @click="data.favoriteTeams = data.favoriteTeams.includes(option) ? data.favoriteTeams.filter((other) => other !== option) : [...data.favoriteTeams, option].slice(0, 5)">
            {{ option }}

            <span style="display: inline-block; flex-grow: 1" />

            <svg v-if="data.favoriteTeams.includes(option)" style="fill: #FBBCA2; width: 1rem; margin-right: 1.2rem;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22ZM11.0026 16L18.0737 8.92893L16.6595 7.51472L11.0026 13.1716L8.17421 10.3431L6.75999 11.7574L11.0026 16Z"></path></svg>
          </p>
        </div>
      </transition>
    </div>

    <p class="input-label" style="padding-top: 2rem;">
      What is your email?
    </p>

    <input v-model="data.email" type="email" class="text-input" placeholder="baron@davis.com">

    <p class="input-label" style="padding-top: 2rem;">
      Do you want to see betting lines?
    </p>

    <div style="display: flex; flex-direction: row; justify-content: center; align-items: center">
      <span class="caption-text" style="margin-right: .5rem" :style="{color: data.includeBets ? '#747B94' : '#fff'}">No</span>
      <input class="switch" type="checkbox" v-model="data.includeBets">
      <span class="caption-text" style="margin-left: .5rem" :style="{color: !data.includeBets ? '#747B94' : '#fff'}">Yes</span>
    </div>

    <button @click="submit" class="button" :class="data.email.length > 1 && data.email.includes('@') && data.favoriteTeams.length > 0 && data.favoriteLeagues.length > 0 ? '' : 'button-off'">
      Get personalized news
    </button>
  </div>
</template>

<script lang="ts">
/* eslint-disable */
import {defineComponent, onMounted, reactive, ref} from 'vue';

export default defineComponent({
  name: 'App',
  setup() {
    const data = reactive({
      email: '',
      includeBets: true,
      favoriteLeagues: [],
      favoriteTeams: [],
    });
    const favoriteTeamOptions = [
      "Arizona Cardinals",
      "Atlanta Falcons",
      "Baltimore Ravens",
      "Buffalo Bills",
      "Carolina Panthers",
      "Chicago Bears",
      "Cincinnati Bengals",
      "Cleveland Browns",
      "Dallas Cowboys",
      "Denver Broncos",
      "Detroit Lions",
      "Green Bay Packers",
      "Houston Texans",
      "Indianapolis Colts",
      "Jacksonville Jaguars",
      "Kansas City Chiefs",
      "Las Vegas Raiders",
      "Los Angeles Chargers",
      "Los Angeles Rams",
      "Miami Dolphins",
      "Minnesota Vikings",
      "New England Patriots",
      "New Orleans Saints",
      "New York Giants",
      "New York Jets",
      "Philadelphia Eagles",
      "Pittsburgh Steelers",
      "San Francisco 49ers",
      "Seattle Seahawks",
      "Tampa Bay Buccaneers",
      "Tennessee Titans",
      "Washington Football Team",
      "Arizona Diamondbacks",
      "Atlanta Braves",
      "Baltimore Orioles",
      "Boston Red Sox",
      "Chicago White Sox",
      "Chicago Cubs",
      "Cincinnati Reds",
      "Cleveland Guardians",
      "Colorado Rockies",
      "Detroit Tigers",
      "Houston Astros",
      "Kansas City Royals",
      "Los Angeles Angels",
      "Los Angeles Dodgers",
      "Miami Marlins",
      "Milwaukee Brewers",
      "Minnesota Twins",
      "New York Yankees",
      "New York Mets",
      "Oakland Athletics",
      "Philadelphia Phillies",
      "Pittsburgh Pirates",
      "San Diego Padres",
      "San Francisco Giants",
      "Seattle Mariners",
      "St. Louis Cardinals",
      "Tampa Bay Rays",
      "Texas Rangers",
      "Toronto Blue Jays",
      "Washington Nationals",
      "Atlanta Hawks",
      "Boston Celtics",
      "Brooklyn Nets",
      "Charlotte Hornets",
      "Chicago Bulls",
      "Cleveland Cavaliers",
      "Dallas Mavericks",
      "Denver Nuggets",
      "Detroit Pistons",
      "Golden State Warriors",
      "Houston Rockets",
      "Indiana Pacers",
      "LA Clippers",
      "Los Angeles Lakers",
      "Memphis Grizzlies",
      "Miami Heat",
      "Milwaukee Bucks",
      "Minnesota Timberwolves",
      "New Orleans Pelicans",
      "New York Knicks",
      "Oklahoma City Thunder",
      "Orlando Magic",
      "Philadelphia 76ers",
      "Phoenix Suns",
      "Portland Trail Blazers",
      "Sacramento Kings",
      "San Antonio Spurs",
      "Toronto Raptors",
      "Utah Jazz",
      "Washington Wizards",
    ];
    const favoriteLeagueOptions = [
      'NBA',
      'NFL',
      'MLB',
    ];
    const isShowingTeams = ref(false);
    const isShowingLeagues = ref(false);
    const query = ref('');

    onMounted(() => {
      window.addEventListener('click', (e) => {
        if (!document.getElementById('teams')!.contains(e.target as HTMLElement)) {
          isShowingTeams.value = false;
          query.value = '';
        }

        if (!document.getElementById('leagues')!.contains(e.target as HTMLElement)) {
          isShowingLeagues.value = false;
        }
      });

      window.addEventListener('keydown', (e) => {
        if (isShowingTeams.value) {
          if (e.key === ' ' || e.key === 'Delete' || e.key === 'Backspace') {
            query.value = '';
          } else {
            query.value = e.key;
          }
        }
      });
    });

    async function submit() {
      const response = await fetch('http://localhost:3000', {
        method: 'POST',
        headers: {
          accept: 'application/json',
          'content-type': 'application/json',
        },
        body: JSON.stringify(data),
      });
    }

    return {
      data,
      favoriteTeamOptions,
      favoriteLeagueOptions,
      isShowingTeams,
      isShowingLeagues,
      query,
      submit,
    }
  },
});
</script>

<style>
body, #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #fff;
  margin-top: 60px;
  background-color: #060B1C;
  min-height: 100%;
}

.text-input {
  background-color: #292D3D;
  border: solid 1.5px #747B94;
  border-radius: 8px;
  padding: .6rem 1.2rem .6rem 1.2rem;
  min-width: 15rem;
  max-width: 15rem;
  display: inline-block;
  color: #fff;
  font-size: 16px;
}

.text-input::placeholder {
  color: #747B94;
}

.select-dropdown {
  position: absolute;
  top: 100%;
  background-color: #292D3D;
  border: solid 1.5px #747B94;
  width: 100%;
  left: 0;
  border-radius: 8px;
  margin-top: 10px;
  max-height: 15rem;
  overflow-y: scroll;
  z-index: 5;
}

.caption-text {
  font-weight: 400;
  font-size: 15px;
}

.input-label {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: .75rem;
}

.switch {
  position: relative;
  height: 1.5rem;
  width: 3rem;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  border-radius: 9999px;
  background-color: rgba(100, 116, 139, 0.377);
  transition: all .3s ease;
}

.switch:checked {
  background-color: #FBBCA2;
}

.switch::before {
  position: absolute;
  content: "";
  left: calc(1.5rem - 1.6rem);
  top: calc(1.5rem - 1.6rem);
  display: block;
  height: 1.6rem;
  width: 1.6rem;
  cursor: pointer;
  border: 1px solid rgba(100, 116, 139, 0.527);
  border-radius: 9999px;
  background-color: rgba(255, 255, 255, 1);
  box-shadow: 0 3px 10px rgba(100, 116, 139, 0.327);
  transition: all .3s ease;
}

.switch:hover::before {
  box-shadow: 0 0 0px 8px rgba(0, 0, 0, .15)
}

.switch:checked:hover::before {
  box-shadow: 0 0 0px 8px rgba(251, 188, 162, .15)
}

.hover-bg {
  transition: all ease-in-out 250ms;
  border-radius: 8px;
  padding: .3rem .6rem .3rem .6rem;
  margin: .3rem .6rem .3rem .6rem;
}

.hover-bg:hover {
  background-color: #383C4E;
}

.switch:checked:before {
  transform: translateX(100%);
  border-color: #FBBCA2;
}

.button {
  transition: all ease-in-out 300ms;
  cursor: pointer; margin-top: 2rem; background-color: #FBBCA2; padding: 1rem 3rem 1rem 3rem; border: none; outline: none; border-radius: 8px; font-weight: 600; font-size: 16px;

  transform: translateY(0);
  opacity: 1;
}

.button-off {
  transform: translateY(100%);
  opacity: 0;
}

.button:hover {
  background-color: #E9A588;
}

</style>
