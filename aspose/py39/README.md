# How to use it

|- A/ (or folder you want)
  |- pdf/

```sh
docker run --rm -it \
  -v A/:/workspace \
  -e FROM_EXT=pdf \
  -e TO_EXT=md \
  aspose:py39
```
