Kivy Study
==========

Refreshing myself with the basics of Kivy once more.


## Kivy Official Docs

Best for API references.

https://kivy.org/doc/stable/guide/basic.html


### Projects

- https://github.com/kivy/kivy/wiki/List-of-Kivy-Projects


### KV Lang

It's possible to add some "scripting" to our kv files using the the
[pyexpander](https://pyexpander.sourceforge.io/introduction.html) module.

This will allow us to have dynamic elements added to our kv files much like any html templating
language (i.e. Jinja2)

- [Syntax Reference](https://pyexpander.sourceforge.io/reference-expander.html#syntax-of-the-pyexpander-language)
- [KV Lang Pre-processing doc](https://github.com/kivy/kivy/wiki/Kv-language-preprocessing)


## Inclem Kivy Crash Course

I've found these tutorials a better way to get introduced to working with Kivy
vs the official docs.

http://inclem.net/pages/kivy-crash-course/

https://github.com/inclement/kivycrashcourse


## Entity Component Systems

ECS seems like a very sound architecture for creating games. I like that it follows the
seperation of concerns principle much like a typical MVC/MTV pattern widely used in
web development.

- https://en.wikipedia.org/wiki/Entity_component_system
- https://austinmorlan.com/posts/entity_component_system/
- https://tsprojectsblog.wordpress.com/portfolio/entity-component-system/
- http://t-machine.org/index.php/2007/09/03/entity-systems-are-the-future-of-mmog-development-part-1/

### Entity component systems and you: They're not just for game developers

- [O'Reilly Software Architecture 2019 Talk](https://conferences.oreilly.com/software-architecture/sa-ny-2019/public/schedule/detail/71964.html)
- [Blog](https://hey.paris/2019/02/08/software-architecture-nyc-2019/)
- [Video](https://youtu.be/SFKR5rZBu-8)
- [Slides](notes/ecs_and_you_talk.pdf)

### Seba's Lab

- http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/
- http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/
- http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/


### Python implementations

- https://github.com/benmoran56/esper
- https://python-utilities.readthedocs.io/en/latest/ebs.html
- https://github.com/seanfisk/ecs
- https://github.com/kivy/KivEnt


## Kivy Notes

## [KivEnt](https://github.com/kivy/KivEnt)

KivEnt is a highly performant ECS game engine for Kivy. It appears to still be in active development
however, if you're planning to release your kivy game for mobile, its p4a recipe is currently
broken.

I've tried building it from the `update_recipes` branch of its source but it didn't work for me. I
might be able to make it work if I fix the sys.path issues (there's an error about unable to import
Kivy on the build step) I am getting but it is beyond my understanding at the moment.

Perhaps it would be nice to simply adopt its architecture using purely just Kivy?


## Building for Mobile

- [Kivy Buildozer Docs](https://kivy.org/doc/stable/guide/packaging-android.html?highlight=buildozer#buildozer)
- [Buildozer Docs](https://buildozer.readthedocs.io/en/latest/installation.html)
- [Buildozer Source](https://github.com/kivy/buildozer)
- [Creating a Release APK](https://github.com/kivy/kivy/wiki/Creating-a-Release-APK)

### Command reference (Android)

Buildozer requires that you have a `main.py` as your application's entrypoint.

You will need to run the ff. commands from within your kivy project.


#### Initialize

```
buildozer init
```

Then edit the `buildozer.spec` file.


#### Deploy and run

```
buildozer -v android debug deploy run
```


#### Troubleshooting

When buildozer does not auto-install the Android SDKs

```
buildozer appclean
buildozer distclean
buildozer android debug
```
