package main

import (
	"fmt"

	"github.com/nozzle/throttler"

	"github.com/ernestosuarez/itertools"
)

type card struct {
	faces [4]int
	name  byte
}

const (
	THREADS = 8
	MAX     = 362880.0

	BU = 1
	BD = -1
	RU = 2
	RD = -2
	GU = 3
	GD = -3
	PU = 4
	PD = -4
)

var cardsInitial = [9]card{
	{name: 'a', faces: [4]int{BD, RD, PU, GU}},
	{name: 'b', faces: [4]int{PD, GD, BU, RU}},
	{name: 'c', faces: [4]int{BD, GD, BU, RU}},
	{name: 'd', faces: [4]int{PD, RD, BU, GU}},
	{name: 'e', faces: [4]int{PD, RD, PU, GU}},
	{name: 'f', faces: [4]int{BD, RD, PU, GU}},
	{name: 'g', faces: [4]int{RU, GD, BD, PU}},
	{name: 'h', faces: [4]int{PU, GD, RD, BU}},
	{name: 'i', faces: [4]int{PU, BU, RD, GD}},
}

var cardsList = []int{0, 1, 2, 3, 4, 5, 6, 7, 8}

func getRotMatrix() [][]int {
	ret := [][]int{}
	a := []int{0, 0, 0, 0, 0, 0, 0, 0, 0}
	i := 0

	for {
		b := make([]int, len(a))
		copy(b, a)
		ret = append(ret, b)
		a[i] += 1

		for {
			if a[i] == 4 {
				a[i] = 0
				i += 1
				if i == 9 {
					return ret
				}
				a[i] += 1
				continue
			}
			i = 0
			break
		}
	}

	return ret
}

func rotate(c card, n int) card {
	tmp := [4]int{c.faces[0], c.faces[1], c.faces[2], c.faces[3]}
	for i := 0; i < n; i++ {
		tmp = [4]int{
			tmp[3],
			tmp[0],
			tmp[1],
			tmp[2],
		}
	}
	return card{name: c.name, faces: tmp}
}

func rotateAll(m []int, cards [9]card) [9]card {
	for i, c := range cards {
		cards[i] = rotate(c, m[i])
	}

	return cards
}

func validate(cards [9]card) bool {
	// Top row
	if cards[0].faces[1] != cards[1].faces[3]*-1 {
		return false
	}
	if cards[1].faces[1] != cards[2].faces[3]*-1 {
		return false
	}

	// Second row across
	if cards[3].faces[1] != cards[4].faces[3]*-1 {
		return false
	}
	if cards[4].faces[1] != cards[5].faces[3]*-1 {
		return false
	}
	// Second row up
	if cards[3].faces[0] != cards[0].faces[2]*-1 {
		return false
	}
	if cards[4].faces[0] != cards[1].faces[2]*-1 {
		return false
	}
	if cards[5].faces[0] != cards[2].faces[2]*-1 {
		return false
	}

	// Third row across
	if cards[6].faces[1] != cards[7].faces[3]*-1 {
		return false
	}
	if cards[7].faces[1] != cards[8].faces[3]*-1 {
		return false
	}
	// Third row up
	if cards[6].faces[0] != cards[3].faces[2]*-1 {
		return false
	}
	if cards[7].faces[0] != cards[4].faces[2]*-1 {
		return false
	}
	if cards[8].faces[0] != cards[5].faces[2]*-1 {
		return false
	}

	return true
}

func prettyFaces(faces [4]int) string {
	str := ""
	for _, f := range faces {
		code := "xx"
	
		if f == 1 {
			code = "BU"
		} else if f == -1 {
			code = "BD"
		} else if f == 2 {
			code = "RU"
		} else if f == -2 {
			code = "RD"
		} else if f == 3 {
			code = "GU"
		} else if f == -3 {
			code = "GD"
		} else if f == 4 {
			code = "PU"
		} else if f == -4 {
			code = "PD"
		}

		str = fmt.Sprintf("%s %s", str, code)
	}
	return str
}

func main() {

	rotMatrix := getRotMatrix()
	outerCount := 0

	for _ = range itertools.PermutationsInt(cardsList, len(cardsList)) {
		outerCount++
	}

	// fmt.Printf("TOTAL: %d\n", outerCount*len(rotMatrix))
	// TOTAL: 95126814720

	th := throttler.New(32, outerCount)

	outerCount = 0
	for cardsOrder := range itertools.PermutationsInt(cardsList, len(cardsList)) {
		outerCount++
		go func(outerCount int) {

			fmt.Printf("%d / %0.0f (%0.2f)\n", outerCount, MAX, ((float64(outerCount) / MAX) * 100.0))

			cards := [9]card{}

			for i, n := range cardsOrder {
				// fmt.Printf("DEBUG: %v %v\n", i, n)
				cards[i] = cardsInitial[n]
			}

			for _, m := range rotMatrix {
				// fmt.Printf("B: %v\n", cards)
				tmp := rotateAll(m, cards)
				// fmt.Printf("A: %v\n", cards)
				// fmt.Printf("T: %v\n", tmp)

				if validate(tmp) {
					for _, c := range tmp {
						fmt.Printf("%c: %s\n", c.name, prettyFaces(c.faces))
					}
					th.Done(fmt.Errorf("TEST"))
					return
				}
			}
			th.Done(nil)
		}(outerCount)

		if errCount := th.Throttle(); errCount > 0 {
			fmt.Println(th.Err())
			return
		}
	}
}
