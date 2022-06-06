# How to update dependencies

Dependencies in the NodeJS world change constantly and packages get outdated
quite fast. Usually you could keep things as they were originally developed,
but this being a high-load, user-facing app, you need to take care of new
found vulnerabilities. Use the following as a guide (not fullproof) to update
the dependencies.

Start with installing the following package globally, in order to check for
outdated versions. Then run it in the frontend folder and a full list of
outdated dependencies will be shown, along with the latest. **Attention**:
Never automatically update all deps at one time, unless they all have only patch
changes.

```sh
# Install globally
npm i -g npm-check-updates

# List outdated
ncu

# Update a specific package
ncu -f NAME_OF_THE_PACKAGE -i
```

Then you can interactively choose a single package to update manually, in
interactive mode. The guideline is to always check if the version change is
major/minor/patch (shown by which part of the version number changed).

For **minor** or **patch** changes, it is generally easy to update automatically
to the latest, but you might want to check the release notes on the package's
GitHub page (which you can access directly from NPM). For **major** changes,
always check if the peer dependencies changed, if the release notes deprecate
an API or if they have an upgrade guide.


## Historical update

Date: *20th Jun 2021*

- removed `vue-awesome` and replaced with `@fortawesome` icons
- removed chart related dependencies
- replaced `vue-native-websocket` with `vue-simple-websocket`
- update `webpack` from 2.6 to 4.46 and some related dependencies
- updated webpack dev and prod configs
- update `eslint` from 4.18 to 7.28
- updated eslint config
- replaced `eslint-plugin-standard` with `eslint-plugin-vue`
- refactored the code to be valid with `eslint-plugin-vue`
- update `bootstrap` from 4.0.0-beta.2 to 4.5.3
- update `bootstrap-vue` from 2.0.0-rc.20 to 2.21.2

