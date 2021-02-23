export default {
  categories: [
    {
      name: 'Colour Perception',
      id: 'cp',
      color: 'cat-one',
      icon: 'palette',
      evaluation: 'good',
      score: '30',
      metrics: ['m1']
    },
    {
      name: 'Perceptual Fluency',
      id: 'pf',
      color: 'cat-two',
      icon: 'brain',
      evaluation: 'okay',
      score: '30',
      metrics: ['m2']
    },
    {
      name: 'Visual Guidance',
      id: 'vg',
      color: 'cat-three',
      icon: 'compass',
      evaluation: 'bad',
      score: '30',
      metrics: []
    },
    {
      name: 'Accessibility',
      id: 'ac',
      color: 'cat-four',
      icon: 'universal-access',
      evaluation: 'bad',
      score: '30',
      metrics: []
    }
  ],
  metrics: {
    m1: {
      id: 'm1',
      name: 'PNG File Size',
      category: 'cp',
      description:
        'File size in PNG indicates the number of effectively used colors. The higher the size, the more colourful the image is likely to be. Note that this is confounded by other factors, such as image complexity.',
      evidence: 1,
      relevance: 2,
      speed: 2,
      evaluation: 'good',
      visualizationType: 'table',
      references: [
        {
          title:
            'Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.',
          fileName: 'miniukovich_and_de_angeli_2015.pdf'
        }
      ],
      results: [
        {
          id: 'm1_0',
          index: 0,
          type: 'int',
          name: 'PNG File Size (in bytes)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0, 500000],
              description: 'Suitable',
              icon: ['far', 'check-circle'],
              judgment: 'good'
            },
            {
              id: 'r2',
              range: [500001, 1200000],
              description: 'Fair',
              icon: [null, null],
              judgment: 'normal'
            },
            {
              id: 'r3',
              range: [1200001, null],
              description: 'Huge',
              icon: ['fas', 'exclamation-triangle'],
              judgment: 'bad'
            }
          ]
        }
      ]
    },
    m2: {
      id: 'm2',
      name: 'JPG File Size',
      category: 'pf',
      description:
        'JPG file size has some association with clutter perception. However, little evidence exists, and the metric is confounded by other factors.',
      evidence: 2,
      relevance: 3,
      speed: 2,
      evaluation: 'good',
      visualizationType: 'table',
      references: [
        {
          title:
            'Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.',
          fileName: 'miniukovich_and_de_angeli_2015.pdf'
        }
      ],
      results: [
        {
          id: 'm2_0',
          index: 0,
          type: 'int',
          name: 'JPG File Size (in bytes)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0, 100000],
              description: 'Suitable',
              icon: ['far', 'check-circle'],
              judgment: 'good'
            },
            {
              id: 'r2',
              range: [100001, 200000],
              description: 'Fair',
              icon: [null, null],
              judgment: 'normal'
            },
            {
              id: 'r3',
              range: [200001, null],
              description: 'Huge',
              icon: ['fas', 'exclamation-triangle'],
              judgment: 'bad'
            }
          ]
        }
      ]
    }
  }
}
