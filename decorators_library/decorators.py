import time
from .exceptions import TimeoutError
import logging
import sys
import webbrowser

def timeout(fnparam):
    def timeoutfn(fn):
        def starttimeout(*args, **kwargs):
            starttime = time.time()
            result = fn()
            endtime = time.time()
            diff = endtime - starttime
            if diff > fnparam:
                raise TimeoutError('Function call timed out')
            return result    
        return starttimeout        
    return timeoutfn

def debug(logger=None): #check for logger
    def debuggin(original_function):
        def func_wrapper(*args, **kwargs):
            if logger is None:
                l = logging.getLogger(original_function.__module__)
            else:
                l = logger
            l.debug("Executing \"{0}\" with params: {1}, {2}".format(original_function.__name__, args, kwargs))
            result = original_function(*args)
            l.debug("Finished \"{0}\" execution with result: {1}".format(original_function.__name__, result))
            return result
        return func_wrapper
    return debuggin


class count_calls(object):
    counterdict = {}

    def __init__(self, fn):
        self.fn = fn
        self.func_name = self.fn.__name__
        if not self.func_name in self.counterdict:
            self.counterdict[self.func_name] = 0
        
    def __call__(self, *args, **kwargs):
        self.counterdict[self.func_name] += 1
        return self.fn(*args, **kwargs)
    
    def counter(self):
        return self.counterdict[self.func_name]

    @classmethod
    def counters(cls):
        return cls.counterdict
    
    @classmethod
    def reset_counters(cls):
        cls.counterdict = {}

class memoized(object):
    cache = {}
    
    def __init__(self,original_function):
        self.original_function = original_function
        
    def __call__(self, *args, **kwargs):
        if args in self.cache:
            return self.cache[args]
        else: 
            resultreturn = self.original_function(*args, **kwargs)
            self.cache.update({args:resultreturn})
            return resultreturn

# Extra Decorators!

def time_benchmark(fn):
    def start_time_benchmark(*args, **kwargs):
        starttime = time.time()
        result = fn(*args, **kwargs)
        endtime = time.time()
        diff = endtime - starttime
        difftime = time.gmtime(diff)
        diffseconds = time.strftime("%S s", difftime)
        return "Result: {}, Time taken: {}".format(result, diffseconds)
    return start_time_benchmark
    

def multiplier(n):
    def multiply_by_n(fn):
        def multiply_fn_by_n(arg):
            return arg * n
        return multiply_fn_by_n
    return multiply_by_n

def pokedex(fn):
    pokedex_list = ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'Squirtle',
    'Wartortle', 'Blastoise', 'Caterpie', 'Metapod', 'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 
    'Pidgey', 'Pidgeotto', 'Pidgeot', 'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok', 
    'Pikachu', 'Raichu', 'Sandshrew', 'Sandslash', 'Nidoran-f', 'Nidorina', 'Nidoqueen', 'Nidoran',
    'Nidorino', 'Nidoking', 'Clefairy', 'Clefable', 'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 
    'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume', 'Paras', 'Parasect', 'Venonat', 'Venomoth', 
    'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck', 'Mankey', 'Primeape', 'Growlithe', 
    'Arcanine', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'Machop', 'Machoke', 
    'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 
    'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro', 'Magnemite', 'Magneton', "Farfetch'd", 'Doduo', 
    'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 
    'Onix', 'Drowzee', 'Hypno', 'Krabby', 'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 
    'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 
    'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 'Staryu', 'Starmie', 
    'Mr. Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Gyarados', 
    'Lapras', 'Ditto', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kabuto', 
    'Kabutops', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dratini', 'Dragonair', 
    'Dragonite', 'Mewtwo']
    def a_pokemon(arg):
        if arg in pokedex_list:
            return "{} is a Pokemon!".format(arg)
        else:
            return "{} is not a Pokemon :(".format(arg)
    return a_pokemon    
