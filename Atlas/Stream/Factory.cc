// This file may be redistributed and modified under the terms of
// the GNU Lesser General Public License (See COPYING for details).
// Copyright (C) 2000 Michael Day

#include "Factory.h"

using namespace std;
using namespace Atlas::Stream;

template <typename T>
list<Factory<T>*> Factory<T>::factories;
