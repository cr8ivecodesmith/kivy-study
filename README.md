Kivy Study
==========

Refreshing myself with the basics of Kivy once more.


## Kivy Official Docs

Best for API references.

https://kivy.org/doc/stable/guide/basic.html


## Inclem Kivy Crash Course

I've found these tutorials a better way to get introduced to working with Kivy
vs the official docs.

http://inclem.net/pages/kivy-crash-course/

https://github.com/inclement/kivycrashcourse


## Entity Component Systems

- https://github.com/kivy/KivEnt
- https://en.wikipedia.org/wiki/Entity_component_system

### Seba's Lab

- http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iii-entity-component-systems/
- http://www.sebaslab.com/the-truth-behind-inversion-of-control-part-iv-dependency-inversion-principle/
- http://www.sebaslab.com/ecs-design-to-achieve-true-inversion-of-flow-control/


## Building for Mobile

- [Kivy Buildozer Docs](https://kivy.org/doc/stable/guide/packaging-android.html?highlight=buildozer#buildozer)
- [Buildozer Docs](https://buildozer.readthedocs.io/en/latest/installation.html)
- [Buildozer Source](https://github.com/kivy/buildozer)

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
