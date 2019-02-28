const fs = require('fs')
const path = require('path')

function main () {
  const inputPath = process.argv[2]
  const inputStr = String(fs.readFileSync(inputPath))
  const [photoCountStr, ...lines] = inputStr.split('\n')
  const photoCount = Number(photoCountStr)
  const photos = lines.filter(Boolean).map((l, id) => {
    const [ori, tagCountStr, ...tags] = l.split(' ')
    const tagCount = Number(tagCountStr)
    const isVert = ori === 'V'
    return { isVert, tagCount, tags, id }
  })
  console.log(photoCount)
  // photos

  const slides = []
  for (let i = 0; i < photos.length; i++) {
    const photo = photos[i]
    if (photo.isVert) {
      for (let j = i + 1; j < photos.length; j++) {
        if (photos[j].isVert) {
          slides.push(`${photo.id} ${photos[j].id}`)
          photos.splice(j, 1)
          break
        }
      }
    } else {
      slides.push(photo.id)
    }
  }

  console.log(slides)
  let result = []
  result.push(slides.length)
  result = result.concat(slides)
  fs.writeFileSync('./' + path.basename(inputPath) + '.out' , result.join('\n'))
}

main()
